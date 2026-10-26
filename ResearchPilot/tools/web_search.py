from dataclasses import dataclass

from ddgs import DDGS
from ddgs.exceptions import DDGSException


class WebSearchError(RuntimeError):
    """Raised when the web search service cannot return usable results."""


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    content: str


class DuckDuckGoSearchTool:
    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Search query must not be empty.")
        if not 1 <= max_results <= 20:
            raise ValueError("max_results must be between 1 and 20.")

        try:
            with DDGS(timeout=self.timeout) as search_client:
                raw_results = search_client.text(query, max_results=max_results)
        except DDGSException as error:
            raise WebSearchError(f"DuckDuckGo search failed: {error}") from error

        results = []
        for item in raw_results:
            if not isinstance(item, dict):
                continue
            url = item.get("href") or item.get("url")
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                continue
            results.append(
                SearchResult(
                    title=str(item.get("title") or url),
                    url=url,
                    content=str(item.get("body") or item.get("content") or ""),
                )
            )
        return results
