"""
Browserbase / Stagehand web tools for the ReportAgent.

Exposes three AI-native browser tools that the agent can call:
  - browse_web:       navigate to a URL and perform a natural-language action
  - extract_web_data: navigate and extract structured data from a page
  - observe_web:      discover actionable elements or answer a query about a page

Falls back silently (is_available() → False) when BROWSERBASE_ENABLED is false
or the API credentials are absent, so the agent simply doesn't see these tools.
"""

from typing import Optional
from ..config import Config
from ..utils.logger import get_logger

logger = get_logger('mirofish.web_tools')


class WebToolsService:
    """Stagehand-backed web browsing tools for the ReportAgent."""

    def __init__(self):
        self._stagehand = None
        self._page = None

        if not self.is_available():
            logger.info("Browserbase web tools disabled (BROWSERBASE_ENABLED=false or missing keys)")
            return

        try:
            from stagehand import Stagehand, StagehandConfig
            cfg = StagehandConfig(
                env="BROWSERBASE",
                api_key=Config.BROWSERBASE_API_KEY,
                project_id=Config.BROWSERBASE_PROJECT_ID,
            )
            self._stagehand = Stagehand(cfg)
            logger.info("Browserbase / Stagehand web tools initialised")
        except Exception as e:
            logger.warning(f"Browserbase init failed, web tools disabled: {e}")
            self._stagehand = None

    def is_available(self) -> bool:
        return (
            Config.BROWSERBASE_ENABLED
            and bool(Config.BROWSERBASE_API_KEY)
            and bool(Config.BROWSERBASE_PROJECT_ID)
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_page(self):
        """Lazily initialise the Stagehand page/session."""
        if self._stagehand is None:
            raise RuntimeError("Stagehand client not initialised")
        if self._page is None:
            self._stagehand.init()
            self._page = self._stagehand.page
        return self._page

    def _navigate(self, url: str):
        page = self._get_page()
        page.goto(url)
        return page

    # ------------------------------------------------------------------
    # Public tool methods  (all return plain text for the ReACT loop)
    # ------------------------------------------------------------------

    def browse_web(self, url: str, instruction: str) -> str:
        """
        Navigate to *url* and perform *instruction* using Stagehand act().
        Returns a text description of what happened / was observed.
        """
        try:
            page = self._navigate(url)
            result = page.act(instruction)
            return f"[browse_web] URL: {url}\nInstruction: {instruction}\nResult: {result}"
        except Exception as e:
            logger.warning(f"browse_web error: {e}")
            return f"[browse_web] Error accessing {url}: {e}"

    def extract_web_data(self, url: str, schema_description: str) -> str:
        """
        Navigate to *url* and extract structured data matching *schema_description*
        using Stagehand extract(). Returns extracted content as text.
        """
        try:
            page = self._navigate(url)
            result = page.extract(schema_description)
            return f"[extract_web_data] URL: {url}\nExtracted:\n{result}"
        except Exception as e:
            logger.warning(f"extract_web_data error: {e}")
            return f"[extract_web_data] Error extracting from {url}: {e}"

    def observe_web(self, url: str, query: str) -> str:
        """
        Navigate to *url* and run *query* through Stagehand observe() to
        discover actionable elements or answer questions about the page.
        """
        try:
            page = self._navigate(url)
            result = page.observe(query)
            return f"[observe_web] URL: {url}\nQuery: {query}\nObservations:\n{result}"
        except Exception as e:
            logger.warning(f"observe_web error: {e}")
            return f"[observe_web] Error observing {url}: {e}"

    def close(self):
        """Close the Stagehand session (call when the agent run finishes)."""
        if self._stagehand is not None:
            try:
                self._stagehand.close()
            except Exception:
                pass
            self._page = None
