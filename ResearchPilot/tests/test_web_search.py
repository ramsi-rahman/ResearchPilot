import pytest

from tools.web_search import DuckDuckGoSearchTool


def test_search_maps_duckduckgo_results(monkeypatch) -> None:
    class FakeDDGS:
        def __init__(self, timeout: int) -> None:
            assert timeout == 7

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            pass

        def text(self, query: str, max_results: int) -> list[dict[str, str]]:
            assert query == "battery storage"
            assert max_results == 2
            return [
                {
                    "title": "Battery research",
                    "href": "https://example.com/battery",
                    "body": "Research summary",
                },
                {"title": "Invalid result", "href": "javascript:alert(1)"},
            ]

    monkeypatch.setattr("tools.web_search.DDGS", FakeDDGS)
    results = DuckDuckGoSearchTool(timeout=7).search("battery storage", 2)

    assert len(results) == 1
    assert results[0].title == "Battery research"
    assert results[0].url == "https://example.com/battery"
    assert results[0].content == "Research summary"


@pytest.mark.parametrize(
    ("query", "max_results", "message"),
    [
        ("  ", 5, "query must not be empty"),
        ("valid query", 0, "max_results must be between 1 and 20"),
    ],
)
def test_search_rejects_invalid_arguments(
    query: str, max_results: int, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        DuckDuckGoSearchTool().search(query, max_results)
