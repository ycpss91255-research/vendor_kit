"""hook 共用：找 repo 的主 worktree 與 worktree 根目錄。

CLAUDE_PROJECT_DIR 可能是主 worktree，也可能是 linked worktree（session 開在
worktree/pr/<編號> 之類的地方）。linked worktree 的 .git 是檔案，內容是
gitdir: <主 worktree>/.git/worktrees/<名>，從這裡回推主 worktree。
"""
import os
import re
from pathlib import Path


def main_dir() -> Path:
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    dotgit = project / ".git"
    if dotgit.is_file():
        m = re.match(r"gitdir:\s*(.+)", dotgit.read_text(errors="ignore").strip())
        if m:
            gitdir = Path(m.group(1))
            gitdir = gitdir if gitdir.is_absolute() else project / gitdir
            gitdir = gitdir.resolve()
            if gitdir.parent.name == "worktrees":
                return gitdir.parent.parent.parent
    return project


def worktree_root() -> Path:
    """所有 worktree 的固定位置：主 worktree 上一層的 worktree/。"""
    return main_dir().parent / "worktree"
