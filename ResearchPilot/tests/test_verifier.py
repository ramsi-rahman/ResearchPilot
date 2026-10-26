from agent.analyst import Analysis, Finding
from agent.researcher import ResearchSource
from agent.verifier import verify


def test_verify_accepts_finding_with_matching_http_source() -> None:
    source = ResearchSource(
        title="Example source",
        url="https://example.com/article",
        content="Source text",
        search_snippet="Snippet",
    )
    analysis = Analysis(
        findings=[
            Finding(
                title="Example source",
                excerpt="Source text",
                source_url=source.url,
            )
        ]
    )

    result = verify(analysis, [source])

    assert result.verified
    assert result.warnings == []


def test_verify_warns_when_finding_has_no_matching_source() -> None:
    analysis = Analysis(
        findings=[
            Finding(
                title="Orphan finding",
                excerpt="Some text",
                source_url="https://example.com/missing",
            )
        ]
    )

    result = verify(analysis, [])

    assert not result.verified
    assert any("No search results" in warning for warning in result.warnings)
    assert any("no matching research source" in warning for warning in result.warnings)
