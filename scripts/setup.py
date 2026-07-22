"""Windows Pitfalls setup — auto-configure pyrite for this project."""

import os
import sys
from pathlib import Path

# Project root is parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PYRITE_CONFIG_DIR = Path.home() / ".pyrite"
CONFIG_FILE = PYRITE_CONFIG_DIR / "config.yaml"
INDEX_PATH = PROJECT_ROOT / "data" / "index"


def main():
    PYRITE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = f"""knowledge_bases:
- name: windows-pitfalls
  path: {PROJECT_ROOT.as_posix()}
  kb_type: reference
  description: Windows 避坑指南
settings:
  index_path: {INDEX_PATH.as_posix()}
  enable_mcp: true
"""

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(config)

    print(f"Config written to: {CONFIG_FILE}")
    print(f"  KB path: {PROJECT_ROOT}")
    print(f"  Index:   {INDEX_PATH}")

    # Build index
    print("\nBuilding index...")
    sys.path.insert(0, str(PROJECT_ROOT))
    from pyrite.config import load_config
    from pyrite.storage.database import PyriteDB
    from pyrite.storage.index import IndexManager

    # Ensure index dir exists
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    c = load_config()
    db = PyriteDB(c.settings.index_path)
    indexer = IndexManager(db, c)
    count = indexer.index_kb("windows-pitfalls")
    db.close()

    print(f"Indexed {count} entries.\n")
    print("Setup complete. Start the MCP server with:")
    print(f"  cd {PROJECT_ROOT}")
    print("  python -m pyrite.server.mcp_server --tier admin")


if __name__ == "__main__":
    main()
