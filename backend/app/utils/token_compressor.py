"""
The Token Company — prompt compression middleware.

Compresses user/system message content before LLM calls to reduce token usage
and cost. Falls back silently (no-op) when disabled or the key is absent.
"""

from typing import Dict, Any, List, Optional
from ..config import Config
from .logger import get_logger

logger = get_logger('mirofish.token_compressor')

_compressor_instance = None


class TokenCompressor:
    """Wraps The Token Company SDK for prompt compression."""

    def __init__(self):
        self._client = None
        self._enabled = Config.TOKEN_COMPANY_ENABLED and bool(Config.TOKEN_COMPANY_API_KEY)

        if self._enabled:
            try:
                from the_token_company import TokenCompany
                self._client = TokenCompany(api_key=Config.TOKEN_COMPANY_API_KEY)
                logger.info("Token Company compression enabled")
            except Exception as e:
                logger.warning(f"Token Company init failed, compression disabled: {e}")
                self._enabled = False

    def compress_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Compress user/system message content in-place (returns new list).
        Skips messages shorter than TOKEN_COMPANY_MIN_CHARS and assistant messages.
        """
        if not self._enabled or self._client is None:
            return messages

        compressed = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role in ("user", "system") and isinstance(content, str) and len(content) >= Config.TOKEN_COMPANY_MIN_CHARS:
                try:
                    result = self._client.compress(content)
                    compressed_text = result.compressed_text if hasattr(result, "compressed_text") else str(result)
                    ratio = getattr(result, "compression_ratio", None)
                    saved = getattr(result, "tokens_saved", None)
                    logger.debug(
                        f"Token Company: role={role} ratio={ratio} tokens_saved={saved}"
                    )
                    compressed.append({**msg, "content": compressed_text})
                    continue
                except Exception as e:
                    logger.warning(f"Token Company compression error (using original): {e}")

            compressed.append(msg)

        return compressed


def get_compressor() -> TokenCompressor:
    """Return the singleton TokenCompressor instance."""
    global _compressor_instance
    if _compressor_instance is None:
        _compressor_instance = TokenCompressor()
    return _compressor_instance
