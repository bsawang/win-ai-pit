"""CLI for Windows Pitfalls — system-level MCP server management."""

import argparse
import subprocess
import sys
from pathlib import Path


def _get_data_dir() -> Path:
    """Get the system-level data directory (~/.windows-pitfalls/)."""
    return Path.home() / ".windows-pitfalls"


def _get_pyrite_config_dir() -> Path:
    """Get pyrite config directory (~/.pyrite/)."""
    return Path.home() / ".pyrite"


def _get_pyrite_config_file() -> Path:
    """Get pyrite config file path."""
    return _get_pyrite_config_dir() / "config.yaml"


def _get_data_index_path() -> Path:
    """Get the index path within the data directory."""
    return _get_data_dir() / "data" / "index"


def _get_claude_settings() -> Path:
    """Get global Claude Code settings file."""
    return Path.home() / ".claude" / "settings.json"


GITHUB_REPO = "https://github.com/bsawang/win-ai-pit.git"


def cmd_init(args):
    """Initialize ~/.windows-pitfalls/ and configure global MCP."""
    data_dir = _get_data_dir()
    pyrite_cfg = _get_pyrite_config_file()
    claude_settings = _get_claude_settings()

    if data_dir.exists():
        print(f"数据目录已存在: {data_dir}")
        overwrite = input("重新初始化？(y/N): ").lower().strip()
        if overwrite != "y":
            print("跳过")
            return
        shutil.rmtree(data_dir)

    # Clone repo as data directory (keep .git for sync capability)
    print(f"克隆仓库到 {data_dir} ...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", GITHUB_REPO, str(data_dir)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"克隆失败: {result.stderr}")
        sys.exit(1)
    print("克隆完成")

    # Set up remote for sync (origin → GitHub)
    # .git is kept so git pull/push work out of the box

    # Write pyrite config
    _get_pyrite_config_dir().mkdir(parents=True, exist_ok=True)
    config_content = f"""knowledge_bases:
- name: windows-pitfalls
  path: {data_dir.as_posix()}
  kb_type: reference
  description: Windows 避坑指南
settings:
  index_path: {_get_data_index_path().as_posix()}
  enable_mcp: true
"""
    pyrite_cfg.write_text(config_content, encoding="utf-8")
    print(f"配置写入: {pyrite_cfg}")

    # Build index
    print("重建索引...")
    sys.path.insert(0, str(data_dir))
    from pyrite.config import load_config
    from pyrite.storage.database import PyriteDB
    from pyrite.storage.index import IndexManager

    _get_data_index_path().parent.mkdir(parents=True, exist_ok=True)
    c = load_config()
    db = PyriteDB(c.settings.index_path)
    indexer = IndexManager(db, c)
    count = indexer.index_kb("windows-pitfalls")
    db.close()
    print(f"索引完成: {count} 条")

    # Write global Claude MCP config
    claude_settings.parent.mkdir(parents=True, exist_ok=True)
    mcp_config = {
        "mcpServers": {
            "windows-pitfalls": {
                "description": "Windows 避坑指南 — search_pitfall / record_pitfall",
                "command": "windows-pitfalls",
                "args": ["start"],
            }
        }
    }
    import json
    if claude_settings.exists():
        existing = json.loads(claude_settings.read_text(encoding="utf-8"))
        existing.setdefault("mcpServers", {})
        existing["mcpServers"]["windows-pitfalls"] = mcp_config["mcpServers"]["windows-pitfalls"]
        claude_settings.write_text(
            json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        claude_settings.write_text(
            json.dumps(mcp_config, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(f"Claude MCP 配置写入: {claude_settings}")

    print("\n初始化完成！任意目录下打开 Claude Code，MCP Server 自动启动。")
    print(f"数据目录: {data_dir}")


def cmd_start(args):
    """Start MCP Server in stdio mode (for Claude Code auto-start or manual use).

    Auto-detects mode:
    - System-level: ~/.windows-pitfalls/ exists → use global config
    - Project-level: running from repo root → use local pitfalls
    """
    data_dir = _get_data_dir()
    project_root = Path.cwd()

    # Check if we're in the project repo with local pitfalls
    is_project_mode = (project_root / "pitfalls").exists() and (project_root / "kb.yaml").exists()

    if not is_project_mode and not data_dir.exists():
        print("错误: 未找到数据目录。请先运行: windows-pitfalls init", file=sys.stderr)
        sys.exit(1)

    from pyrite.server.mcp_server import main as mcp_main
    sys.argv = ["mcp_server.py", "--tier", args.tier or "admin"]
    mcp_main()


def cmd_log(args):
    """View activity log."""
    log_file = _get_data_dir() / "data" / "activity.log"
    if not log_file.exists():
        print("暂无活动记录")
        return
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    # Show last N lines (default 20)
    n = args.n or 20
    for line in lines[-n:]:
        print(line)


def cmd_index(args):
    """Rebuild index from data directory."""
    from pyrite.config import load_config
    from pyrite.storage.database import PyriteDB
    from pyrite.storage.index import IndexManager

    data_dir = _get_data_dir()
    if not data_dir.exists():
        print(f"错误: 数据目录不存在 {data_dir}")
        print("请先运行: windows-pitfalls init")
        sys.exit(1)

    c = load_config()
    db = PyriteDB(c.settings.index_path)
    indexer = IndexManager(db, c)
    count = indexer.index_kb("windows-pitfalls")
    db.close()
    print(f"索引重建完成: {count} 条")


def main():
    parser = argparse.ArgumentParser(prog="windows-pitfalls")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="初始化数据目录和全局配置")
    start_p = sub.add_parser("start", help="启动 MCP Server（stdio 模式）")
    start_p.add_argument("--tier", choices=["read", "write", "admin"], default="admin")
    sub.add_parser("index", help="重建索引")
    log_p = sub.add_parser("log", help="查看活动日志")
    log_p.add_argument("-n", type=int, default=20, help="显示行数")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "start":
        cmd_start(args)
    elif args.command == "index":
        cmd_index(args)
    elif args.command == "log":
        cmd_log(args)


if __name__ == "__main__":
    main()
