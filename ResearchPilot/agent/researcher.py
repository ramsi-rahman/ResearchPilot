from dataclasses import dataclass

from tools.web_search import DuckDuckGoSearchTool, SearchResult
from tools.webpage_reader import WebpageReadError, WebpageReader


@dataclass(frozen=True)
class ResearchSource:
    title: str
    url: str
    content: str
    search_snippet: str
    read_error: str | None = None


class Researcher:
    def __init__(
        self,
        search_tool: DuckDuckGoSearchTool,
        webpage_reader: WebpageReader,
    ) -> None:
        self.search_tool = search_tool
        self.webpage_reader = webpage_reader

    def research(self, query: str, max_results: int) -> list[ResearchSource]:
        results = self.search_tool.search(query, max_results)
        return [self._read_result(result) for result in results]

    def _read_result(self, result: SearchResult) -> ResearchSource:
        try:
            page_content = self.webpage_reader.read(result.url)
            content = page_content or result.content
            read_error = None
        except WebpageReadError as error:
            content = result.content
            read_error = str(error)
        return ResearchSource(
            title=result.title,
            url=result.url,
            content=content,
            search_snippet=result.content,
            read_error=read_error,
        )
