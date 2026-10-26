import pytest

from agent.planner import create_plan


def test_create_plan_normalizes_question_whitespace() -> None:
    plan = create_plan("  How   do batteries\nstore energy? ")

    assert plan.question == "How do batteries store energy?"
    assert plan.search_query == plan.question


def test_create_plan_rejects_empty_question() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        create_plan(" \n ")
