from html.parser import HTMLParser

import requests


class WebpageReadError(RuntimeError):
    """Raised when a source webpage cannot be fetched or parsed."""


class _TextExtractor(HTMLParser):
    _IGNORED_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self._IGNORED_TAGS:
            self._ignored_depth += 1
        elif tag in {"p", "div", "br", "li", "h1", "h2", "h3"}:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._IGNORED_TAGS and self._ignored_depth:
            self._ignored_depth -= 1
        elif tag in {"p", "div", "br", "li", "h1", "h2", "h3"}:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)


class WebpageReader:
    def __init__(self, timeout: int = 20, max_characters: int = 12000) -> None:
        self.timeout = timeout
        self.max_characters = max_characters

    def read(self, url: str) -> str:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "ResearchPilot/1.0 (+source research)"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise WebpageReadError(f"Could not read {url}: {error}") from error

        parser = _TextExtractor()
        try:
            parser.feed(response.text)
        except Exception as error:
            raise WebpageReadError(f"Could not parse webpage {url}: {error}") from error
        text = " ".join(" ".join(parser.parts).split())
        return text[: self.max_characters]
