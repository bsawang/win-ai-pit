"""Windows Pitfalls plugin for pyrite."""

from pathlib import Path
from typing import Any, ClassVar

from pyrite.plugins.capabilities import Capability


class WindowsPitfallsPlugin:
    """Windows 避坑指南插件 — 提供 Windows 踩坑知识的检索与记录。"""

    name = "windows_pitfalls"
    capabilities: ClassVar[set[Capability]] = {
        Capability.SCHEMA,
        Capability.SURFACE,
        Capability.DOMAIN,
        Capability.CONTEXT,
    }

    def __init__(self):
        self.ctx = None

    def set_context(self, ctx) -> None:
        self.ctx = ctx

    def get_field_schemas(self) -> dict[str, dict[str, dict]]:
        """Define rich field schemas for windows_pitfall type."""
        return {
            "windows_pitfall": {
                "symptom": {
                    "type": "text",
                    "required": True,
                    "description": "现象描述",
                },
                "root_cause": {
                    "type": "text",
                    "description": "根因简述",
                },
                "environment": {
                    "type": "text",
                    "description": '环境信息 JSON: {"os":[],"tool":"","tool_versions":[]}',
                },
                "solution": {
                    "type": "text",
                    "description": "简要解法",
                },
                "severity": {
                    "type": "select",
                    "options": ["critical", "medium", "low"],
                    "default": "medium",
                },
                "tags": {
                    "type": "tags",
                    "description": "分类标签",
                },
            }
        }

    def get_mcp_tools(self, tier: str) -> dict[str, dict]:
        """Register MCP tools for the given tier."""
        tools = {}

        if tier in ("read", "write", "admin"):
            tools["search_pitfall"] = {
                "description": "搜索 Windows 避坑记录。按症状、工具、操作系统等条件匹配已知坑。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词，描述遇到的问题",
                        },
                        "tool": {
                            "type": "string",
                            "description": "相关工具（如 msys, cmd, powershell, python）",
                        },
                        "os": {
                            "type": "string",
                            "description": "操作系统版本",
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "medium", "low"],
                            "description": "按严重程度过滤",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回结果数量上限",
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                },
                "handler": self._handle_search_pitfall,
            }

        if tier in ("write", "admin"):
            tools["record_pitfall"] = {
                "description": "记录一个新的 Windows 避坑条目。会自动检查是否已存在类似条目（去重）。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "坑的标题，一句话概括",
                        },
                        "symptom": {
                            "type": "string",
                            "description": "现象描述 — 出什么问题了",
                        },
                        "root_cause": {
                            "type": "string",
                            "description": "根因 — 为什么会出现这个问题",
                        },
                        "solution": {
                            "type": "string",
                            "description": "解决方案或绕过方式",
                        },
                        "os": {
                            "type": "string",
                            "description": "操作系统版本",
                        },
                        "tool": {
                            "type": "string",
                            "description": "相关工具",
                        },
                        "tool_versions": {
                            "type": "string",
                            "description": "工具版本（逗号分隔）",
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "medium", "low"],
                            "default": "medium",
                        },
                        "tags": {
                            "type": "string",
                            "description": "标签（逗号分隔）",
                        },
                    },
                    "required": ["title", "symptom", "solution"],
                },
                "handler": self._handle_record_pitfall,
            }

        return tools

    @staticmethod
    def _get_repo_root(config) -> Path:
        """Get the git repo root (KB path)."""
        return config.knowledge_bases[0].path

    @staticmethod
    def _git_run(args: list[str], repo_path: Path) -> tuple[bool, str]:
        """Run a git command. Returns (success, stdout)."""
        try:
            import subprocess
            r = subprocess.run(
                ["git"] + args, cwd=repo_path,
                capture_output=True, text=True, timeout=30,
            )
            return r.returncode == 0, r.stdout.strip()
        except Exception:
            return False, ""

    @staticmethod
    def _git_try_sync(repo_path: Path) -> bool:
        """git fetch → if new commits → pull. Returns True if pulled."""
        ok, out = WindowsPitfallsPlugin._git_run(["remote"], repo_path)
        if not ok or not out.strip():
            return False
        # Try lightweight fetch first
        WindowsPitfallsPlugin._git_run(["fetch", "--depth", "1"], repo_path)
        # Check if there are updates
        ok, count = WindowsPitfallsPlugin._git_run(
            ["rev-list", "--count", "HEAD..origin/HEAD"], repo_path
        )
        if ok and count.strip() and int(count.strip()) > 0:
            ok, _ = WindowsPitfallsPlugin._git_run(["pull", "--ff-only"], repo_path)
            return ok
        return False

    @staticmethod
    def _git_commit_and_push(repo_path: Path, file_rel: str, title: str) -> bool:
        """git add + commit + push. Fail silently if not a git repo."""
        ok1, _ = WindowsPitfallsPlugin._git_run(["add", file_rel], repo_path)
        if not ok1:
            return False
        ok2, _ = WindowsPitfallsPlugin._git_run(
            ["commit", "-m", f"record: {title}"], repo_path
        )
        if not ok2:
            return False
        ok3, _ = WindowsPitfallsPlugin._git_run(["remote"], repo_path)
        if ok3:
            WindowsPitfallsPlugin._git_run(["push"], repo_path)
        return True

    def _handle_search_pitfall(self, arguments: dict) -> dict:
        """Search for pitfalls matching the given criteria."""
        from pyrite.config import load_config
        from pyrite.storage.database import PyriteDB

        config = load_config()
        db = PyriteDB(config.settings.index_path)

        try:
            query = arguments.get("query", "")
            tool_filter = arguments.get("tool")
            os_filter = arguments.get("os")
            severity = arguments.get("severity")
            limit = arguments.get("limit", 10)

            # Sanitize query for FTS5 (handles > / - etc.)
            from pyrite.services.search_service import SearchService
            sanitized = SearchService.sanitize_fts_query(query)

            service = SearchService(db)

            def _search(q: str) -> list[dict]:
                return service.search(
                    q, kb_name="windows-pitfalls",
                    entry_type="windows_pitfall", limit=limit,
                )

            results = _search(sanitized)

            # If no results, try git fetch + pull + reindex + retry
            if not results:
                repo_path = self._get_repo_root(config)
                if self._git_try_sync(repo_path):
                    # Rebuild index after pull
                    from pyrite.storage.index import IndexManager
                    IndexManager(db, config).index_kb("windows-pitfalls")
                    results = _search(sanitized)

            # Post-filter by tool/os/severity
            import json as _json

            def _get_meta(r):
                m = r.get("metadata", {})
                return _json.loads(m) if isinstance(m, str) else m

            filtered = []
            for r in results:
                meta = _get_meta(r)

                if tool_filter:
                    env = meta.get("environment", {})
                    env_str = str(env.get("tool", "")) + str(env.get("tool_versions", ""))
                    if tool_filter not in env_str:
                        continue
                if os_filter:
                    env = meta.get("environment", {})
                    if os_filter not in str(env.get("os", [])):
                        continue
                if severity and meta.get("severity") != severity:
                    continue

                filtered.append(r)

            text = _json.dumps(filtered[:limit], ensure_ascii=False, default=str, indent=2)
            return {"content": [{"type": "text", "text": text}]}

        finally:
            db.close()

    def _handle_record_pitfall(self, arguments: dict) -> dict:
        """Record a new pitfall entry with dedup check."""
        import json
        from pyrite.config import load_config
        from pyrite.storage.database import PyriteDB

        config = load_config()
        db = PyriteDB(config.settings.index_path)

        try:
            title = arguments.get("title", "")
            symptom = arguments.get("symptom", "")
            root_cause = arguments.get("root_cause", "")
            solution = arguments.get("solution", "")
            os_val = arguments.get("os", "")
            tool = arguments.get("tool", "")
            tool_versions = arguments.get("tool_versions", "")
            severity = arguments.get("severity", "medium")
            tags_str = arguments.get("tags", "")

            # Build environment metadata
            env = {}
            if os_val:
                env["os"] = [os_val]
            if tool:
                env["tool"] = tool
            if tool_versions:
                env["tool_versions"] = [v.strip() for v in tool_versions.split(",")]

            # === Dedup: search existing entries for similar title/symptom ===
            from pyrite.services.search_service import SearchService

            service = SearchService(db)

            # Stop words that don't carry meaningful signal for dedup
            # (single Chinese chars + common English stop words)
            _STOP_WORDS = frozenset({
                '的', '了', '在', '是', '有', '和', '就', '不', '都',
                '一', '个', '上', '也', '很', '到', '要', '去', '会',
                '着', '好', '这', '他', '她', '它', '们', '时',
                '中', '与', '为', '之', '及', '等', '或', '但', '被', '从', '以',
                '对', '把', '向', '让', '用', '将', '并', '而', '且', '于', '其',
                '所', '该', '各', '每', '哪', '那', '着',
                'the', 'a', 'an', 'is', 'are', 'was', 'were',
                'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                'will', 'would', 'can', 'could', 'shall', 'should', 'may', 'might',
                'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
                'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
                'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
                'about', 'up', 'down',
            })

            def _significant_words(text: str, max_n: int = 15) -> set:
                """Extract meaningful tokens for dedup comparison.

                English: word-level tokens, filtered by stop words and len > 1.
                Chinese: character-level tokens (each char is a token), filtered by stop chars.
                Mixed text: handles both in the same string.
                """
                import re as _re
                result = []
                for token in _re.split(r'[\s,，。；;：:！!？?、/()（）【】\[\]{}"\']+', text.lower()):
                    token = token.strip(".,:;!?\"'<>@#￥$%^&*+-=～·、，。；：！？（）【】《》〈〉『』〔〕")
                    if not token:
                        continue

                    # Detect CJK characters by Unicode range
                    has_cjk = any('一' <= c <= '鿿' for c in token)

                    if has_cjk:
                        # Chinese: individual characters as tokens
                        for c in token:
                            if c not in _STOP_WORDS and not c.isspace():
                                result.append(c)
                                if len(result) >= max_n:
                                    return set(result)
                    else:
                        # English: word-level
                        if token not in _STOP_WORDS and len(token) > 1:
                            result.append(token)
                            if len(result) >= max_n:
                                return set(result)
                return set(result)

            def _overlap_ratio(a: set, b: set) -> float:
                """Jaccard-like overlap: |intersection| / |max(a,b)|."""
                if not a or not b:
                    return 0.0
                return len(a & b) / max(len(a), len(b))

            # Try searching by title first (sanitized for FTS5)
            query = SearchService.sanitize_fts_query(title)
            existing = service.search(
                query,
                kb_name="windows-pitfalls",
                entry_type="windows_pitfall",
                limit=5,
            )

            # Fallback: if FTS5 returned nothing (special chars / short query),
            # extract meaningful keywords and search again
            if not existing:
                import re as _re
                keywords = [
                    w for w in _re.sub(r'[^\w\s]', ' ', title).split()
                    if w.lower() not in _STOP_WORDS and len(w) > 1
                ]
                if keywords:
                    fallback_query = " OR ".join(keywords[:5])
                    existing = service.search(
                        fallback_query,
                        kb_name="windows-pitfalls",
                        entry_type="windows_pitfall",
                        limit=5,
                    )

            # Fallback 2: list recent entries as last resort
            if not existing:
                existing = service.search(
                    "",
                    kb_name="windows-pitfalls",
                    entry_type="windows_pitfall",
                    limit=5,
                )

            for r in existing:
                meta_raw = r.get("metadata", {})
                meta = json.loads(meta_raw) if isinstance(meta_raw, str) else meta_raw
                existing_title = r.get("title", "")
                existing_symptom = meta.get("symptom", "")

                title_sig = _significant_words(title, 8)
                existing_title_sig = _significant_words(existing_title, 8)
                symptom_sig = _significant_words(symptom, 15)
                existing_symptom_sig = _significant_words(existing_symptom, 15)

                title_score = _overlap_ratio(title_sig, existing_title_sig)
                symptom_score = _overlap_ratio(symptom_sig, existing_symptom_sig)

                # Dedup decision:
                # - Strong match in either title (>0.5) or symptom (>0.5) alone is enough
                # - Moderate match in BOTH (>0.25 each) also triggers dedup
                # - Pure symptom match without ANY title overlap is not trusted (avoids false positives)
                if (
                    title_score > 0.5
                    or (title_score > 0.25 and symptom_score > 0.25)
                    or (symptom_score > 0.5 and title_score > 0.1)
                ):
                    result = {
                        "status": "skipped",
                        "reason": "类似条目已存在",
                        "existing_entry_id": meta.get("id", ""),
                        "existing_title": existing_title,
                    }
                    return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}

            # === No duplicate found, create the entry ===
            import re
            import uuid

            entry_id = re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-")
            if not entry_id:
                entry_id = f"pitfall-{uuid.uuid4().hex[:8]}"

            from pyrite.models.generic import GenericEntry

            body = f"""## 症状

{symptom}

## 根因

{root_cause}

## 解决

{solution}
"""

            tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]

            entry = GenericEntry(
                id=entry_id,
                title=title,
                body=body,
                tags=tags_list,
                _entry_type="windows_pitfall",
                metadata={
                    "type": "windows_pitfall",
                    "symptom": symptom,
                    "root_cause": root_cause,
                    "solution": solution,
                    "environment": env,
                    "severity": severity,
                },
            )

            # Save using pyrite's repository
            from pyrite.storage.repository import KBRepository

            repo = KBRepository(config.knowledge_bases[0])
            repo.save(entry)

            # Rebuild index so this entry is immediately searchable
            from pyrite.storage.index import IndexManager
            indexer = IndexManager(db, config)
            indexed = indexer.index_kb("windows-pitfalls")

            # Git commit + push (silent, best-effort)
            repo_path = self._get_repo_root(config)
            file_rel = f"pitfalls/{entry_id}.md"
            self._git_commit_and_push(repo_path, file_rel, title)

            result = {
                "status": "created",
                "entry_id": entry_id,
                "title": title,
            }
            return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}

        finally:
            db.close()
