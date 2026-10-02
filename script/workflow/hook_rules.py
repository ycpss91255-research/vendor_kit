"""共用 .claude/hooks/comment_tag_guard.py 與 attribution_guard.py 的規則，給 script/workflow/ 的其他腳本 import。

用途：
  本文自檢（body.py）、之後的留言檔準備（prepare_comment.py）要跟 hook 用同一套規則
  （本機絕對路徑樣式、留言標記、[codex]／[agy] 原文的註記行）；merge 前的署名檢查（merge_pr.py）
  要跟 attribution_guard.py 用同一組 BANNED。規則只寫在 hook 裡，
  這裡直接載入 hook 模組再匯出，不另抄一份；hook 改了，這些腳本自動跟著變。

用法（模組，沒有命令列介面）：
  import hook_rules
  hook_rules.LOCAL_PATHS            # ((compiled re, 標籤), ...)
  hook_rules.tagged(text)           # 第一行是否以 [claude]／[codex]／[agy] 開頭
  hook_rules.local_path_problem(text, src, raw_ok)
  hook_rules.BANNED                 # attribution_guard.py 的 Claude 署名樣式（compiled re）
  hook_rules.load(path, names)      # 從指定路徑載入 hook 模組（測試用）

匯出：LOCAL_PATHS、TAGS、RAW_TAGS、NOTE_PREFIXES、tagged、local_path_problem（comment_tag_guard）；
BANNED（attribution_guard）。

錯誤：hook 檔不存在或載入失敗時 raise HookRulesError，訊息寫明找不到哪個檔；
不會退回自己的副本。這是模組，不輸出 JSON、沒有結束碼。
"""
import importlib.util
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / ".claude/hooks/comment_tag_guard.py"
NAMES = ("LOCAL_PATHS", "TAGS", "RAW_TAGS", "NOTE_PREFIXES", "tagged", "local_path_problem")
ATTRIBUTION_HOOK = HOOK.with_name("attribution_guard.py")
ATTRIBUTION_NAMES = ("BANNED",)


class HookRulesError(ImportError):
    """載不到 hook 檔的規則。"""


def load(path: Path = HOOK, names: tuple = NAMES):
    """載入 path 指到的 hook 模組並回傳；缺檔或缺 names 裡的名稱就 raise HookRulesError。"""
    path = Path(path)
    if not path.is_file():
        raise HookRulesError(f"找不到 hook 檔：{path}")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise HookRulesError(f"無法載入 hook 檔：{path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001 — 任何載入錯誤都換成同一種例外
        raise HookRulesError(f"載入 hook 檔失敗：{path}：{e}") from e
    missing = [n for n in names if not hasattr(mod, n)]
    if missing:
        raise HookRulesError(f"hook 檔 {path} 缺少：{'、'.join(missing)}")
    return mod


hook = load()
LOCAL_PATHS = hook.LOCAL_PATHS
TAGS = hook.TAGS
RAW_TAGS = hook.RAW_TAGS
NOTE_PREFIXES = hook.NOTE_PREFIXES
tagged = hook.tagged
local_path_problem = hook.local_path_problem

attribution = load(ATTRIBUTION_HOOK, ATTRIBUTION_NAMES)
BANNED = attribution.BANNED
