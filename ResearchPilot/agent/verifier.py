from dataclasses import dataclass
from urllib.parse import urlparse

from agent.analyst import Analysis
from agent.researcher import ResearchSource


@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    warnings: list[str]


def verify(analysis: Analysis, sources: list[ResearchSource]) -> VerificationResult:
    warnings = []
    source_urls = {source.url for source in sources}

    if not sources:
        warnings.append("No search results were found.")
    if not analysis.findings:
        warnings.append("No readable source excerpts were available.")

    for finding in analysis.findings:
        parsed_url = urlparse(finding.source_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            warnings.append(f"Invalid source URL for finding: {finding.title}")
        if finding.source_url not in source_urls:
            warnings.append(f"Finding has no matching research source: {finding.title}")
        if not finding.excerpt.strip():
            warnings.append(f"Finding has an empty excerpt: {finding.title}")

    return VerificationResult(verified=not warnings, warnings=warnings)
