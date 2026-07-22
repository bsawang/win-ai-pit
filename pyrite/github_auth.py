"""
GitHub auth stub.

Minimal placeholder to satisfy imports when GitHub integration is not used.
"""

import logging

logger = logging.getLogger(__name__)


def get_github_token() -> str | None:
    """Stub: return None since GitHub auth is not configured."""
    return None
