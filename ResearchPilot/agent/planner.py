from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchPlan:
    question: str
    search_query: str


def create_plan(question: str) -> ResearchPlan:
    cleaned_question = " ".join(question.split())
    if not cleaned_question:
        raise ValueError("Research question must not be empty.")
    return ResearchPlan(question=cleaned_question, search_query=cleaned_question)
