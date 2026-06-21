"""
工具模块
"""

from .file_parser import FileParser
from .locale import t, get_locale, set_locale, get_language_instruction

__all__ = ['FileParser', 'LLMClient', 't', 'get_locale', 'set_locale', 'get_language_instruction']


def __getattr__(name):
	if name == 'LLMClient':
		from .llm_client import LLMClient
		return LLMClient
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

