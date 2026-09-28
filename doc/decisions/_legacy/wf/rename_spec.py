#!/usr/bin/env python3
"""v3.1 -> v3.2: 名詞換新名（只改稱呼），code span 與 <sub>…</sub> 不動。"""
import re, sys, pathlib

p = pathlib.Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").split("\n")

# (pattern, replacement) —— 依序套用；只在 code span／<sub> 之外
RULES = [
    (r"工具 repo", "下游 repo"),
    (r"工具 image", "下游 image"),
    (r"工具側 ", "下游 repo 側 "),
    (r"使用者檔四原則", "專案檔四原則"),
    (r"對使用者的檔", "對專案檔"),
    (r"使用者的檔", "專案檔"),
    (r"使用者檔", "專案檔"),
    (r"（使用者的）", "（專案檔）"),
    (r"使用者的；", "專案檔；"),
    (r"需使用者處理", "需人處理"),
    (r"## 1\. 使用者動詞", "## 1. 下游使用者動詞"),
    (r"(?<!下游)使用者(?=改過|、Renovate|刪了| `git|可手改|可編輯|環境|錯誤)", "下游使用者"),
    # 進度日誌／交易日誌 → 進度檔；操作紀錄檔 → 執行紀錄
    (r"進度日誌", "進度檔"),
    (r"交易日誌", "進度檔"),
    (r"操作紀錄檔", "執行紀錄"),
    (r"操作紀錄", "執行紀錄"),
    # frozen → CI 模式
    (r"\bfrozen\b", "CI 模式"),
    # baseline（中文語境）→ 基準版；路徑 baseline/ 與標籤 :baseline 不動
    (r"(?<![:/`\w])baseline(?![/`\w])", "基準版"),
    # 協定號／P → 介面版；schema 號 → 檔案版
    (r"版本／協定／schema 不合", "介面版／檔案版不合"),
    (r"`P` 協定整數", "`P` 介面版整數"),
    (r"`N` schema 整數", "`N` 檔案版整數"),
    (r"協定 <P>", "介面版 <P>"),
    (r"薄殼協定 <P_shell>", "薄殼介面版 <P_shell>"),
    (r"\*\*協定 P\*\*", "**介面版 P**"),
    (r"## 3\. 薄殼 ↔ 引擎協定", "## 3. 薄殼 ↔ 引擎介面"),
    (r"P／schema", "介面版／檔案版"),
    (r"跨 schema", "跨檔案版"),
    (r"schema 遷移", "檔案版遷移"),
    (r"schema 高於", "檔案版高於"),
    (r"讀任一舊 schema", "讀任一舊檔案版"),
    (r"當前 schema", "當前檔案版"),
    (r"同 schema 只加不改", "同檔案版只加不改"),
    (r"支援此 schema 的引擎", "支援此檔案版的引擎"),
    (r"schema <N> 高於本引擎支援的 <M>", "檔案版 <N> 高於本引擎支援的 <M>"),
    (r"schema <N>）", "檔案版 <N>）"),
    (r"## 4\. 檔案 schema", "## 4. 檔案格式（檔案版）"),
    (r"低於支援下限 <floor>", "低於最低介面版 <floor>"),
    # floor → 最低介面版（floor_P、<floor> 不動）
    (r"(?<![<_\w])floor(?![_>\w])", "最低介面版"),
    # 模組名
    (r"引擎 version 模組", "引擎 resolve 模組"),
    (r"引擎 registry 模組", "引擎 resolve 模組"),
    (r"由引擎 launcher-gen 重產", "由引擎 shell 模組重產"),
    # base 只准出現在出處註記
    (r"自 base `dist/script/docker/lib/log\.sh` 移植成 POSIX sh", "自外部 repo 的 `dist/script/docker/lib/log.sh` 移植成 POSIX sh（出處見註記）"),
    (r"移植 base `dist/script/docker/lib/log\.sh` 到 POSIX sh", "移植外部 repo 的 `dist/script/docker/lib/log.sh` 到 POSIX sh（出處見註記）"),
    (r"\*\*P2\*\* base 反向採用", "**P2** 外部 repo（出處註記）反向採用"),
    (r"\| L5 \| 移植 base log\.sh 到 POSIX sh", "| L5 | 移植外部 repo 的 log.sh（出處註記）到 POSIX sh"),
]

# 正規行：只有 version.toml／version.local.toml 的那一行改「版本鎖定行」；config.toml 的 keep／days 正規行不改
LINE_RULES = {
    # (line-substring-to-identify, [(pat, rep)])
}

SPLIT = re.compile(r"(`[^`]*`|<sub>.*?</sub>)")

def apply(seg: str) -> str:
    for pat, rep in RULES:
        seg = re.sub(pat, rep, seg)
    return seg

out = []
in_fence = False
for ln in lines:
    if ln.startswith("```"):
        in_fence = not in_fence
        out.append(ln)
        continue
    if in_fence:
        # 目錄樹／config.toml 範本內的中文說明一併改；JSONL 範例不動
        out.append(ln if ln.startswith("{") else apply(ln))
        continue
    parts = SPLIT.split(ln)
    parts = [apply(s) if i % 2 == 0 else s for i, s in enumerate(parts)]
    out.append("".join(parts))

text = "\n".join(out)

# 正規行 → 版本鎖定行（限 version.toml 語境）
targeted = [
    ("以 §4.1 正規行 regex 於 version.local.toml", "以 §4.1 版本鎖定行 regex 於 version.local.toml"),
    ("version.toml 的 `vendor_kit` 正規行", "version.toml 的 `vendor_kit` 版本鎖定行"),
    ("| 正規行契約 | `vendor_kit` 行**唯一正規形**", "| 版本鎖定行契約 | `vendor_kit` 行**唯一正規形**"),
    ("key regex 與 §4.1 正規行契約共用", "key regex 與 §4.1 版本鎖定行契約共用"),
    ("version.toml 契約 = 唯一正規行（§4.1", "version.toml 契約 = 唯一版本鎖定行（§4.1"),
    ("同 §4.1 正規行精神", "同 §4.1 版本鎖定行精神"),
    ("| 啟動器（每次呼叫，任何動詞） | grep 正規行 | grep `keep`／`days` 正規行 | 讀 vendor.just 自身 | — | grep 正規行 |",
     "| 啟動器（每次呼叫，任何動詞） | grep 版本鎖定行 | grep `keep`／`days` 正規行 | 讀 vendor.just 自身 | — | grep 版本鎖定行 |"),
]
for a, b in targeted:
    if a not in text:
        print("WARN targeted not found:", a[:50], file=sys.stderr)
    text = text.replace(a, b)

# 訊息文字（code span 內）與跨 code span 的句子：整段後處理
post = [
    ("自 base `dist/script/docker/lib/log.sh` 移植成 POSIX sh", "自外部 repo 的 `dist/script/docker/lib/log.sh` 移植成 POSIX sh（出處見註記）"),
    ("移植 base `dist/script/docker/lib/log.sh` 到 POSIX sh", "移植外部 repo 的 `dist/script/docker/lib/log.sh` 到 POSIX sh（出處見註記）"),
    ("`目標引擎 <vY>（協定 <P>、schema <M>）無法無損讀取現有檔（schema <N>）", "`目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）"),
    ("`目前薄殼或引擎低於支援下限 <floor>。", "`目前薄殼或引擎低於最低介面版 <floor>。"),
    ("`無法讀取 <file>：schema <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請使用支援此 schema 的引擎", "`無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請使用支援此檔案版的引擎"),
    ("`薄殼協定 <P_shell> 低於引擎 <vY>", "`薄殼介面版 <P_shell> 低於引擎 <vY>"),
    ("`無法寫入操作紀錄 <path>：<原因>。", "`無法寫入執行紀錄 <path>：<原因>。"),
]
for a, b in post:
    if a not in text:
        print("WARN post not found:", a[:40], file=sys.stderr)
    text = text.replace(a, b)
# 純中文新名旁多餘的空白（原 Latin 詞兩側的空格）
CJK = r"[\u3000-\u9fff\uff00-\uffef（）／、：；。]"
for term in ("基準版", "最低介面版", "進度檔", "執行紀錄", "介面版", "檔案版"):
    text = re.sub("(?<=" + CJK + ") " + term, term, text)
    text = re.sub(term + " (?=" + CJK + ")", term, text)

p.write_text(text, encoding="utf-8")
print("done")
