from datetime import datetime
from pathlib import Path
import re

from agent.analyst import Analysis
from agent.planner import ResearchPlan
from agent.researcher import ResearchSource
from agent.verifier import VerificationResult


def _safe_filename(question: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")
    return (slug[:60].rstrip("-") or "research")


def render_report(
    plan: ResearchPlan,
    analysis: Analysis,
    sources: list[ResearchSource],
    verification: VerificationResult,
    created_at: datetime | None = None,
) -> str:
    created_at = created_at or datetime.now().astimezone()
    status = "Passed" if verification.verified else "Warnings"
    lines = [
        f"# Research report: {plan.question}",
        "",
        f"- Generated: {created_at.isoformat(timespec='minutes')}",
        f"- Verification: {status}",
        "",
        "## Evidence digest",
        "",
    ]

    if analysis.findings:
        for finding in analysis.findings:
            lines.extend(
                [
                    f"### {finding.title}",
                    "",
                    finding.excerpt,
                    "",
                    f"Source: [{finding.source_url}]({finding.source_url})",
                    "",
                ]
            )
    else:
        lines.extend(["No source excerpts were available for this question.", ""])

    if verification.warnings:
        lines.extend(["## Verification notes", ""])
        lines.extend(f"- {warning}" for warning in verification.warnings)
        lines.append("")

    lines.extend(
        [
            "## Method",
            "",
            "This initial version presents excerpts from search results and source "
            "pages. It does not generate or independently establish conclusions. "
            "Check the linked sources before relying on the information.",
            "",
            "## Sources",
            "",
        ]
    )
    if sources:
        lines.extend(
            f"{index}. [{source.title or source.url}]({source.url})"
            for index, source in enumerate(sources, start=1)
        )
    else:
        lines.append("No sources found.")
    lines.append("")
    return "\n".join(lines)


def write_report(
    report_directory: Path,
    plan: ResearchPlan,
    analysis: Analysis,
    sources: list[ResearchSource],
    verification: VerificationResult,
    created_at: datetime | None = None,
) -> Path:
    created_at = created_at or datetime.now().astimezone()
    report_directory.mkdir(parents=True, exist_ok=True)
    timestamp = created_at.strftime("%Y%m%d-%H%M%S")
    report_path = report_directory / f"{timestamp}-{_safe_filename(plan.question)}.md"
    report_path.write_text(
        render_report(plan, analysis, sources, verification, created_at),
        encoding="utf-8",
    )
    return report_path
