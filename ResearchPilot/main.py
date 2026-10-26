import argparse
from datetime import datetime
import sys

from agent.analyst import analyze
from agent.planner import create_plan
from agent.reporter import write_report
from agent.researcher import Researcher
from agent.verifier import verify
from config import get_settings
from storage.database import ResearchDatabase
from tools.web_search import DuckDuckGoSearchTool, WebSearchError
from tools.webpage_reader import WebpageReader


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Research a question and write a cited Markdown digest."
    )
    parser.add_argument("question", nargs="?", help="Question to research")
    parser.add_argument(
        "--history",
        action="store_true",
        help="List recent saved research runs instead of starting a search",
    )
    parser.add_argument("--results", type=int, help="Number of web results (1-20)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = get_settings()
    database = ResearchDatabase(settings.database_path)

    if args.history:
        for run in database.list_runs():
            print(f"{run['id']}: {run['question']} ({run['report_path']})")
        return 0
    if not args.question:
        parser.error("question is required unless --history is used")

    max_results = args.results if args.results is not None else settings.max_results
    if not 1 <= max_results <= 20:
        parser.error("--results must be between 1 and 20")

    try:
        plan = create_plan(args.question)
        researcher = Researcher(
            DuckDuckGoSearchTool(settings.request_timeout),
            WebpageReader(settings.request_timeout, settings.max_page_characters),
        )
        sources = researcher.research(plan.search_query, max_results)
    except (ValueError, WebSearchError) as error:
        print(f"Research failed: {error}", file=sys.stderr)
        return 1

    analysis = analyze(sources)
    verification = verify(analysis, sources)
    created_at = datetime.now().astimezone()
    report_path = write_report(
        settings.report_directory, plan, analysis, sources, verification, created_at
    )
    run_id = database.save_run(plan.question, report_path, sources, created_at)

    print(f"Report: {report_path}")
    print(f"Saved research run: {run_id}")
    if verification.warnings:
        print("Verification warnings:")
        for warning in verification.warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
