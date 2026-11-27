"""Translate new posts on this host and publish them from an isolated worktree."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WORKER = "qwen3.6-nvfp4"
BRANCH = "master"


def git(*args, cwd=ROOT, capture=False):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=capture,
    ).stdout


def model_environment():
    worker = json.loads(subprocess.check_output(["docker", "inspect", WORKER]))[0]
    args = worker["Args"]
    settings = dict(value.split("=", 1) for value in worker["Config"]["Env"])
    key = settings.get("VLLM_API_KEY", "")
    if "--api-key" in args:
        key = args[args.index("--api-key") + 1]
    for arg in args:
        if arg.startswith("--api-key="):
            key = arg.split("=", 1)[1]
    if not key:
        raise RuntimeError("The local model container has no API credential.")
    return {
        **os.environ,
        "LLM_API_KEY": key,
        "LLM_BASE_URL": "http://127.0.0.1:8000/v1",
        "LLM_MODEL": "Qwen3.6-35B-A3B-NVFP4",
    }


def main():
    git("fetch", "origin", BRANCH)
    with tempfile.TemporaryDirectory(prefix="xplore-blog-") as temporary:
        checkout = Path(temporary) / "checkout"
        git("worktree", "add", "--detach", str(checkout), f"origin/{BRANCH}")
        try:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "translate_blog.py"), "--root", str(checkout)],
                env=model_environment(), check=True,
            )
            git("add", "-A", "--", "_data", cwd=checkout)
            if not git("diff", "--cached", "--name-only", cwd=checkout, capture=True):
                return
            git("commit", "-m", "Update English blog translations", cwd=checkout)
            git("push", "origin", f"HEAD:{BRANCH}", cwd=checkout)
        finally:
            git("worktree", "remove", "--force", str(checkout))


if __name__ == "__main__":
    main()
