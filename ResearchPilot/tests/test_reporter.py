from datetime import datetime, timezone

from agent.analyst import Analysis, Finding
from agent.planner import ResearchPlan
from agent.reporter import render_report, write_report
from agent.researcher import ResearchSource
from agent.verifier import VerificationResult


def test_render_report_includes_question_excerpt_citation_and_method() -> None:
    source = ResearchSource(
        title="Battery study",
        url="https://example.com/study",
        content="A source excerpt about batteries.",
        search_snippet="A source excerpt about batteries.",
    )
    report = render_report(
        ResearchPlan("Battery storage", "Battery storage"),
        Analysis(
            [Finding("Battery study", "A source excerpt about batteries.", source.url)]
        ),
        [source],
        VerificationResult(True, []),
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    assert "# Research report: Battery storage" in report
    assert "A source excerpt about batteries." in report
    assert "[https://example.com/study](https://example.com/study)" in report
    assert "does not generate or independently establish conclusions" in report


def test_write_report_creates_markdown_file(tmp_path) -> None:
    plan = ResearchPlan("Battery storage", "Battery storage")
    path = write_report(
        tmp_path,
        plan,
        Analysis([]),
        [],
        VerificationResult(False, ["No sources"]),
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    assert path.exists()
    assert path.suffix == ".md"
    assert "Battery storage" in path.read_text(encoding="utf-8")
