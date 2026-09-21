import json, re, sys, urllib.request, urllib.error
def challenge(host):
    try:
        urllib.request.urlopen(f"https://{host}/v2/")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("WWW-Authenticate")
    return 200, None
def token(hdr, repo):
    m = dict(re.findall(r'(\w+)="([^"]*)"', hdr))
    url = f'{m["realm"]}?service={m["service"]}&scope=repository:{repo}:pull'
    return json.load(urllib.request.urlopen(url)).get("token") or json.load(urllib.request.urlopen(url)).get("access_token")
def get(host, path, tok, method="GET"):
    req = urllib.request.Request(f"https://{host}{path}", method=method, headers={
        "Authorization": f"Bearer {tok}",
        "Accept": ", ".join(["application/vnd.oci.image.index.v1+json","application/vnd.docker.distribution.manifest.list.v2+json","application/vnd.oci.image.manifest.v1+json","application/vnd.docker.distribution.manifest.v2+json"])})
    return urllib.request.urlopen(req)
for host, repo, tag in [("ghcr.io","ycpss91255-docker/toml-bridge",None),("registry.gitlab.com","gitlab-org/gitlab-runner","latest")]:
    code, hdr = challenge(host)
    print(host, code, hdr)
    tok = token(hdr, repo)
    r = get(host, f"/v2/{repo}/tags/list?n=50", tok)
    tags = json.load(r)["tags"]; print(" tags:", tags[:8], "... Link:", r.headers.get("Link"))
    t = tag or tags[-1]
    r = get(host, f"/v2/{repo}/manifests/{t}", tok, "HEAD")
    print(" ", t, r.headers.get("Docker-Content-Digest"), r.headers.get("Content-Type"))
