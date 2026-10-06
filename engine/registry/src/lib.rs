//! GHCR 的 registry client：列 tag、取 tag 指向的 index digest（#28、#372 的 N2 client 與 N59）。
//!
//! 只做 registry API 這一層：發請求、換 token、分頁、分類錯誤。不印診斷、不讀 token 檔、不挑最新版
//! （挑版本用 `imageref::Tag::latest`），錯誤對應到哪個原因代碼由呼叫端決定（見「錯誤分類」）。
//!
//! # 協定
//!
//! 照 Docker Registry 的 token 認證（distribution 的 `docs/spec/auth/token.md`）與 OCI distribution：
//!
//! 1. 先不帶認證請求資源；回 401 時讀 `WWW-Authenticate: Bearer realm=…,service=…,scope=…`。
//! 2. 向 realm 換 bearer token（`?service=…&scope=…`；challenge 沒給 scope 時用
//!    `repository:<路徑>:pull`）。沒帶 token 就匿名換；帶了 token 就用 Basic 認證，帳號是任意非空的
//!    [`USERNAME`]、密碼是 token。這跟 GHCR 文件的 `docker login ghcr.io -u USERNAME --password-stdin`
//!    是同一條路（GitHub Docs「Working with the Container registry」：只支援 personal access token
//!    (classic)，讀取要 `read:packages`）。
//! 3. 帶 `Authorization: Bearer <token>` 重送同一個請求；同一個 [`Repository`] 之後的請求沿用這個 token。
//!
//! realm 必須跟 base URL 同一個來源（scheme、主機、port），否則不送 token、回 [`ErrorKind::Protocol`]。
//!
//! - 列 tag：`GET /v2/<路徑>/tags/list?n=<PAGE_SIZE>`，回應的 `Link: <…>; rel="next"` 有下一頁就繼續，
//!   最多 [`MAX_PAGES`] 頁；下一頁的網址只收同一個來源。
//! - 取 digest：`HEAD /v2/<路徑>/manifests/<tag>`，`Accept` 帶 OCI image index 與 Docker manifest list
//!   （[`INDEX_MEDIA_TYPES`]），讀 `Docker-Content-Digest`。回應的 `Content-Type` 原樣交給呼叫端，
//!   要不要只收多架構 index 由呼叫端判斷。
//!
//! # 只收 ghcr.io
//!
//! image 名稱的 registry 必須是 `imageref::GHCR`（04 registry 與認證）。請求的目的地預設是
//! [`BASE_URL`]；[`Client::with_base_url`] 可注入別的 base URL，給測試的假 registry 用。
//!
//! # 逾時與重試（N59）
//!
//! 連線逾時 [`CONNECT_TIMEOUT`]，單一請求（含讀完回應）逾時 [`REQUEST_TIMEOUT`]。連線失敗、逾時、
//! 429 與 5xx 才重試，一個請求最多試 [`ATTEMPTS`] 次，第 n 次重試前等 [`RETRY_DELAY`] × 2^(n-1)；
//! 401、403、404 與其他狀態不重試。不跟隨轉址。
//!
//! # 錯誤分類
//!
//! [`ErrorKind`] 分五類，呼叫端照 reason_codes.csv 對應：
//!
//! - [`ErrorKind::AuthRequired`]：沒帶 token，registry 要求認證（401／403）。呼叫端對應 VK0001。
//! - [`ErrorKind::TokenRejected`]：帶了 token，換 token 或之後的請求被拒（401／403）。被拒後不改走
//!   匿名重試。呼叫端對應 VK0055。
//! - [`ErrorKind::Network`]：連線失敗、逾時，或重試完仍是 429／5xx。呼叫端對應 VK0055。
//! - [`ErrorKind::NotFound`]：registry 回 404（路徑或 tag 不存在）。
//! - [`ErrorKind::Protocol`]：registry 的回應不合協定（缺 challenge、JSON 不對、digest 格式錯、Link 指到
//!   別的來源、其他狀態碼），以及 image 名稱不是 ghcr.io。
//!
//! 錯誤訊息與任何型別的 `Debug` 都不含 token。
//!
//! # 缺口
//!
//! - 帶 token 的流程照 GHCR 文件與 token 認證規格實作，還沒對私有 package 手動測過（#28 的待辦）；
//!   fine-grained token 與 SSO 的行為以手動測試為準。
//! - ring 要編 C：`vendor_kit` 第一次連到這個 crate（update 查 registry）時，image/Dockerfile 的 test
//!   stage 要加 `musl-tools`，musl 靜態編譯才編得過（#577）。目前只有測試用到，test stage 以主機的
//!   gnu 目標編譯，不受影響。

use std::fmt;
use std::thread;
use std::time::Duration;

use imageref::{Digest, GHCR, Tag};

/// GHCR 的 base URL。
pub const BASE_URL: &str = "https://ghcr.io";
/// 連線逾時。
pub const CONNECT_TIMEOUT: Duration = Duration::from_secs(10);
/// 單一請求的總逾時（含讀完回應）。
pub const REQUEST_TIMEOUT: Duration = Duration::from_secs(30);
/// 一個請求最多試幾次（含第一次）。
pub const ATTEMPTS: u32 = 3;
/// 第一次重試前等多久；之後每次加倍。
pub const RETRY_DELAY: Duration = Duration::from_secs(1);
/// `tags/list` 每頁要幾筆（`n=`）。
pub const PAGE_SIZE: u32 = 100;
/// `tags/list` 最多跟幾頁；超過就當回應不合協定，避免 registry 的 Link 繞圈。
pub const MAX_PAGES: usize = 1000;
/// 帶 token 換 bearer 時的 Basic 帳號；GHCR 接受任意非空帳號（#28）。
pub const USERNAME: &str = "vendor_kit";
/// HEAD manifest 時 `Accept` 帶的 media type：OCI image index、Docker manifest list。
pub const INDEX_MEDIA_TYPES: [&str; 2] = [
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
];

/// 錯誤的類別；對應哪個原因代碼由呼叫端決定（見模組說明）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorKind {
    /// 沒帶 token，registry 要求認證。
    AuthRequired,
    /// 帶了 token，被 registry 拒絕。
    TokenRejected,
    /// 連線失敗、逾時，或重試完仍是 429／5xx。
    Network,
    /// registry 回 404。
    NotFound,
    /// 回應不合協定，或 image 名稱不是 ghcr.io。
    Protocol,
}

/// registry 操作失敗：類別加一句給人看的原因（英文，不含 token）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Error {
    kind: ErrorKind,
    detail: String,
}

impl Error {
    fn new(kind: ErrorKind, detail: impl Into<String>) -> Error {
        Error {
            kind,
            detail: detail.into(),
        }
    }

    pub fn kind(&self) -> ErrorKind {
        self.kind
    }

    /// 原因說明，可填進訊息的 `<reason>`。
    pub fn detail(&self) -> &str {
        &self.detail
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.detail)
    }
}

impl std::error::Error for Error {}

/// registry 讀取用的 token（GHCR 的 personal access token）。`Debug` 不印內容。
#[derive(Clone, PartialEq, Eq)]
pub struct Token(String);

impl Token {
    /// 去掉前後空白；剩下空字串就回 `None`（讀檔得到空內容由呼叫端報錯）。
    pub fn new(s: &str) -> Option<Token> {
        let s = s.trim();
        (!s.is_empty()).then(|| Token(s.to_owned()))
    }
}

impl fmt::Debug for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("Token(<redacted>)")
    }
}

/// HEAD manifest 的結果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Manifest {
    /// `Docker-Content-Digest`。
    pub digest: Digest,
    /// 回應的 `Content-Type`；registry 沒給就是 `None`。
    pub media_type: Option<String>,
}

/// registry client；只決定連到哪裡、逾時與重試。認證狀態在 [`Repository`]。
pub struct Client {
    agent: ureq::Agent,
    /// `scheme://host[:port]`，不含結尾的 `/`。
    base: String,
    attempts: u32,
    retry_delay: Duration,
}

impl Default for Client {
    fn default() -> Client {
        Client::new()
    }
}

impl Client {
    /// 連到 [`BASE_URL`]。
    pub fn new() -> Client {
        Client::build(BASE_URL.to_owned(), REQUEST_TIMEOUT, RETRY_DELAY)
    }

    /// 連到別的 base URL（`http://` 或 `https://` 加主機與可選的 port，不含路徑）；給測試的假 registry 用。
    /// image 名稱仍只收 ghcr.io。
    pub fn with_base_url(base: &str) -> Result<Client, Error> {
        let base = base.trim_end_matches('/');
        let rest = base
            .strip_prefix("https://")
            .or_else(|| base.strip_prefix("http://"));
        match rest {
            Some(host) if !host.is_empty() && !host.contains(['/', '?', '#', '@']) => {
                Ok(Client::build(base.to_owned(), REQUEST_TIMEOUT, RETRY_DELAY))
            }
            _ => Err(Error::new(
                ErrorKind::Protocol,
                format!("invalid registry base URL: {base}"),
            )),
        }
    }

    fn build(base: String, request_timeout: Duration, retry_delay: Duration) -> Client {
        let agent = ureq::Agent::config_builder()
            .timeout_connect(Some(CONNECT_TIMEOUT))
            .timeout_global(Some(request_timeout))
            .http_status_as_error(false)
            .max_redirects(0)
            .build()
            .new_agent();
        Client {
            agent,
            base,
            attempts: ATTEMPTS,
            retry_delay,
        }
    }

    /// 對 `<registry>/<路徑>`（例如 `ghcr.io/acme/tool`）開一個查詢；registry 不是 ghcr.io 或路徑不合就回
    /// [`ErrorKind::Protocol`]。`token` 是 `None` 就匿名查。
    pub fn repository<'a>(
        &'a self,
        image: &str,
        token: Option<&'a Token>,
    ) -> Result<Repository<'a>, Error> {
        let path = match image.split_once('/') {
            Some((GHCR, path)) => path,
            Some((other, _)) => {
                return Err(Error::new(
                    ErrorKind::Protocol,
                    format!("unsupported registry: {other}"),
                ));
            }
            None => {
                return Err(Error::new(
                    ErrorKind::Protocol,
                    format!("unsupported registry: {image}"),
                ));
            }
        };
        if !imageref::is_valid_path(path) {
            return Err(Error::new(
                ErrorKind::Protocol,
                format!("invalid image path: {path}"),
            ));
        }
        Ok(Repository {
            client: self,
            path: path.to_owned(),
            token,
            bearer: None,
        })
    }

    /// 發一個請求；連線失敗、逾時、429、5xx 照常數重試。
    fn send(&self, method: Method, url: &str, headers: &[(&str, &str)]) -> Result<Response, Error> {
        let mut attempt = 1;
        loop {
            let result = self.send_once(method, url, headers);
            let retryable = match &result {
                Ok(r) => r.status == 429 || r.status >= 500,
                Err(_) => true,
            };
            if !retryable {
                return result;
            }
            if attempt >= self.attempts {
                return match result {
                    Ok(r) => Err(Error::new(
                        ErrorKind::Network,
                        format!(
                            "registry returned HTTP {} after {attempt} attempts",
                            r.status
                        ),
                    )),
                    Err(e) => Err(Error::new(
                        ErrorKind::Network,
                        format!("{} (after {attempt} attempts)", e.detail),
                    )),
                };
            }
            thread::sleep(self.retry_delay * 2u32.saturating_pow(attempt - 1));
            attempt += 1;
        }
    }

    fn send_once(
        &self,
        method: Method,
        url: &str,
        headers: &[(&str, &str)],
    ) -> Result<Response, Error> {
        let network = |e: ureq::Error| Error::new(ErrorKind::Network, format!("{url}: {e}"));
        let mut resp = match method {
            Method::Get => {
                let mut req = self.agent.get(url);
                for (k, v) in headers {
                    req = req.header(*k, *v);
                }
                req.call()
            }
            Method::Head => {
                let mut req = self.agent.head(url);
                for (k, v) in headers {
                    req = req.header(*k, *v);
                }
                req.call()
            }
        }
        .map_err(network)?;
        let header = |name: &str| {
            resp.headers()
                .get(name)
                .and_then(|v| v.to_str().ok())
                .map(str::to_owned)
        };
        let status = resp.status().as_u16();
        let www_authenticate = header("www-authenticate");
        let link = header("link");
        let digest = header("docker-content-digest");
        let content_type = header("content-type");
        let body = match method {
            Method::Get => resp.body_mut().read_to_string().map_err(network)?,
            Method::Head => String::new(),
        };
        Ok(Response {
            status,
            www_authenticate,
            link,
            digest,
            content_type,
            body,
        })
    }
}

/// 對一個 image 路徑的查詢；換到的 bearer token 留在這裡給之後的請求用。
pub struct Repository<'a> {
    client: &'a Client,
    path: String,
    token: Option<&'a Token>,
    bearer: Option<String>,
}

impl fmt::Debug for Repository<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Repository")
            .field("base", &self.client.base)
            .field("path", &self.path)
            .field("token", &self.token)
            .field("bearer", &self.bearer.as_ref().map(|_| "<redacted>"))
            .finish()
    }
}

impl Repository<'_> {
    /// 列出全部 tag（照 registry 回的順序，跨頁串起來），不過濾格式。
    pub fn tags(&mut self) -> Result<Vec<String>, Error> {
        let base = &self.client.base;
        let mut url = format!("{base}/v2/{}/tags/list?n={PAGE_SIZE}", self.path);
        let mut tags = Vec::new();
        for _ in 0..MAX_PAGES {
            let resp = self.get_authed(Method::Get, &url, &[])?;
            let json: serde_json::Value = serde_json::from_str(&resp.body).map_err(|e| {
                Error::new(ErrorKind::Protocol, format!("invalid tags/list JSON: {e}"))
            })?;
            match json.get("tags") {
                Some(serde_json::Value::Array(items)) => {
                    for item in items {
                        let tag = item.as_str().ok_or_else(|| {
                            Error::new(ErrorKind::Protocol, "tags/list has a non-string tag")
                        })?;
                        tags.push(tag.to_owned());
                    }
                }
                Some(serde_json::Value::Null) | None => {}
                Some(_) => {
                    return Err(Error::new(
                        ErrorKind::Protocol,
                        "tags/list field \"tags\" is not an array",
                    ));
                }
            }
            let next = match resp.link.as_deref() {
                Some(header) => next_link(header)?,
                None => None,
            };
            match next {
                Some(next) => url = self.same_origin(&next)?,
                None => return Ok(tags),
            }
        }
        Err(Error::new(
            ErrorKind::Protocol,
            format!("tags/list has more than {MAX_PAGES} pages"),
        ))
    }

    /// 取 tag 指向的 manifest digest（期望是多架構 index）。
    pub fn manifest(&mut self, tag: &Tag) -> Result<Manifest, Error> {
        let url = format!("{}/v2/{}/manifests/{tag}", self.client.base, self.path);
        let accept = INDEX_MEDIA_TYPES.join(", ");
        let resp = self.get_authed(Method::Head, &url, &[("Accept", &accept)])?;
        let raw = resp.digest.ok_or_else(|| {
            Error::new(
                ErrorKind::Protocol,
                "manifest response has no Docker-Content-Digest",
            )
        })?;
        let digest = Digest::parse(raw.trim()).ok_or_else(|| {
            Error::new(
                ErrorKind::Protocol,
                format!("invalid Docker-Content-Digest: {raw}"),
            )
        })?;
        Ok(Manifest {
            digest,
            media_type: resp.content_type,
        })
    }

    /// 發請求；沒有 bearer 而遇到 401 時照 challenge 換 token 再送一次，最後分類狀態碼。
    fn get_authed(
        &mut self,
        method: Method,
        url: &str,
        headers: &[(&str, &str)],
    ) -> Result<Response, Error> {
        let mut resp = self.send_with_bearer(method, url, headers)?;
        if resp.status == 401 && self.bearer.is_none() {
            let challenge = resp
                .www_authenticate
                .as_deref()
                .and_then(parse_challenge)
                .ok_or_else(|| {
                    Error::new(
                        ErrorKind::Protocol,
                        "401 without a Bearer WWW-Authenticate challenge",
                    )
                })?;
            self.bearer = Some(self.exchange(&challenge)?);
            resp = self.send_with_bearer(method, url, headers)?;
        }
        match resp.status {
            200..=299 => Ok(resp),
            401 | 403 => Err(self.denied(resp.status)),
            404 => Err(Error::new(
                ErrorKind::NotFound,
                format!("registry returned HTTP 404 for {url}"),
            )),
            s => Err(Error::new(
                ErrorKind::Protocol,
                format!("registry returned HTTP {s} for {url}"),
            )),
        }
    }

    fn send_with_bearer(
        &self,
        method: Method,
        url: &str,
        headers: &[(&str, &str)],
    ) -> Result<Response, Error> {
        let auth = self.bearer.as_ref().map(|b| format!("Bearer {b}"));
        let mut all: Vec<(&str, &str)> = headers.to_vec();
        if let Some(auth) = &auth {
            all.push(("Authorization", auth));
        }
        self.client.send(method, url, &all)
    }

    /// 向 challenge 的 realm 換 bearer token；帶 token 時用 Basic 認證，被拒不改走匿名。
    fn exchange(&self, challenge: &Challenge) -> Result<String, Error> {
        let realm = self.same_origin(&challenge.realm)?;
        let default_scope = format!("repository:{}:pull", self.path);
        let scope = challenge.scope.as_deref().unwrap_or(&default_scope);
        let mut query = vec![format!("scope={}", encode_query(scope))];
        if let Some(service) = &challenge.service {
            query.insert(0, format!("service={}", encode_query(service)));
        }
        let sep = if realm.contains('?') { '&' } else { '?' };
        let url = format!("{realm}{sep}{}", query.join("&"));
        let auth = self
            .token
            .map(|t| format!("Basic {}", base64(format!("{USERNAME}:{}", t.0).as_bytes())));
        let headers: Vec<(&str, &str)> =
            auth.iter().map(|a| ("Authorization", a.as_str())).collect();
        let resp = self.client.send(Method::Get, &url, &headers)?;
        match resp.status {
            200..=299 => {}
            401 | 403 => return Err(self.denied(resp.status)),
            s => {
                return Err(Error::new(
                    ErrorKind::Protocol,
                    format!("token endpoint returned HTTP {s}"),
                ));
            }
        }
        let json: serde_json::Value = serde_json::from_str(&resp.body).map_err(|e| {
            Error::new(
                ErrorKind::Protocol,
                format!("invalid token endpoint JSON: {e}"),
            )
        })?;
        ["token", "access_token"]
            .iter()
            .find_map(|k| json.get(*k).and_then(|v| v.as_str()))
            .filter(|t| !t.is_empty())
            .map(str::to_owned)
            .ok_or_else(|| Error::new(ErrorKind::Protocol, "token endpoint returned no token"))
    }

    fn denied(&self, status: u16) -> Error {
        match self.token {
            Some(_) => Error::new(
                ErrorKind::TokenRejected,
                format!("registry rejected the supplied token (HTTP {status})"),
            ),
            None => Error::new(
                ErrorKind::AuthRequired,
                format!("registry requires read access (HTTP {status})"),
            ),
        }
    }

    /// 相對路徑接到 base URL；絕對網址必須跟 base URL 同一個來源。
    fn same_origin(&self, target: &str) -> Result<String, Error> {
        let base = &self.client.base;
        if target.starts_with('/') && !target.starts_with("//") {
            return Ok(format!("{base}{target}"));
        }
        if target
            .strip_prefix(base.as_str())
            .is_some_and(|rest| rest.starts_with('/'))
        {
            return Ok(target.to_owned());
        }
        Err(Error::new(
            ErrorKind::Protocol,
            format!("registry pointed to another origin: {target}"),
        ))
    }
}

#[derive(Clone, Copy)]
enum Method {
    Get,
    Head,
}

struct Response {
    status: u16,
    www_authenticate: Option<String>,
    link: Option<String>,
    digest: Option<String>,
    content_type: Option<String>,
    body: String,
}

/// `WWW-Authenticate: Bearer realm="…",service="…",scope="…"` 的參數。
#[derive(Debug, PartialEq, Eq)]
struct Challenge {
    realm: String,
    service: Option<String>,
    scope: Option<String>,
}

/// 解析 Bearer challenge；不是 Bearer 或沒有 realm 就回 `None`。
fn parse_challenge(header: &str) -> Option<Challenge> {
    let (scheme, params) = header.trim().split_once(' ')?;
    if !scheme.eq_ignore_ascii_case("bearer") {
        return None;
    }
    let (mut realm, mut service, mut scope) = (None, None, None);
    let mut rest = params.trim();
    while !rest.is_empty() {
        let (key, after) = rest.split_once('=')?;
        let key = key.trim().to_ascii_lowercase();
        let after = after.trim_start();
        let (value, tail) = if let Some(quoted) = after.strip_prefix('"') {
            let end = quoted.find('"')?;
            (&quoted[..end], &quoted[end + 1..])
        } else {
            let end = after.find(',').unwrap_or(after.len());
            (after[..end].trim(), &after[end..])
        };
        match key.as_str() {
            "realm" => realm = Some(value.to_owned()),
            "service" => service = Some(value.to_owned()),
            "scope" => scope = Some(value.to_owned()),
            _ => {}
        }
        rest = tail.trim_start().trim_start_matches(',').trim_start();
    }
    Some(Challenge {
        realm: realm?,
        service,
        scope,
    })
}

/// 從 `Link` 標頭取 `rel="next"` 的網址；沒有 next 就是最後一頁（`None`）。
fn next_link(header: &str) -> Result<Option<String>, Error> {
    for part in header.split(',') {
        let part = part.trim();
        let Some(rest) = part.strip_prefix('<') else {
            continue;
        };
        let Some((url, params)) = rest.split_once('>') else {
            return Err(Error::new(
                ErrorKind::Protocol,
                format!("invalid Link header: {header}"),
            ));
        };
        let is_next = params.split(';').any(|p| {
            let p = p.trim().to_ascii_lowercase();
            p == "rel=\"next\"" || p == "rel=next"
        });
        if is_next {
            return Ok(Some(url.to_owned()));
        }
    }
    Ok(None)
}

/// 查詢字串的值：只留 RFC 3986 的 unreserved 字元與 `:`、`/`，其他百分比編碼。
fn encode_query(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for b in s.bytes() {
        if b.is_ascii_alphanumeric() || matches!(b, b'-' | b'.' | b'_' | b'~' | b':' | b'/') {
            out.push(b as char);
        } else {
            out.push_str(&format!("%{b:02X}"));
        }
    }
    out
}

/// RFC 4648 的 base64（含 `=` 補位），給 Basic 認證用。
fn base64(input: &[u8]) -> String {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::with_capacity(input.len().div_ceil(3) * 4);
    for chunk in input.chunks(3) {
        let b = [
            chunk[0],
            chunk.get(1).copied().unwrap_or(0),
            chunk.get(2).copied().unwrap_or(0),
        ];
        let n = (u32::from(b[0]) << 16) | (u32::from(b[1]) << 8) | u32::from(b[2]);
        for i in 0..4 {
            if i <= chunk.len() {
                out.push(char::from(ALPHABET[((n >> (18 - 6 * i)) & 0x3f) as usize]));
            } else {
                out.push('=');
            }
        }
    }
    out
}

#[cfg(test)]
mod tests;
