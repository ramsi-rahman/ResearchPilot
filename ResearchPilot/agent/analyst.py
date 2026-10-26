from dataclasses import dataclass

from agent.researcher import ResearchSource


@dataclass(frozen=True)
class Finding:
    title: str
    excerpt: str
    source_url: str


@dataclass(frozen=True)
class Analysis:
    findings: list[Finding]


def analyze(sources: list[ResearchSource], excerpt_length: int = 700) -> Analysis:
    findings = []
    for source in sources:
        excerpt = " ".join(source.content.split())[:excerpt_length].strip()
        if excerpt:
            findings.append(
                Finding(
                    title=source.title or source.url,
                    excerpt=excerpt,
                    source_url=source.url,
                )
            )
    return Analysis(findings=findings)
