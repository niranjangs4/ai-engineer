from __future__ import annotations

from engine.llm_reasoning_engine import LLMReasoningEngine


class PlannerAgent:
    def __init__(self, reasoning_engine: LLMReasoningEngine) -> None:
        self.reasoning_engine = reasoning_engine

    def create_plan(self, goal: str) -> list[str]:
        interpreted = self.reasoning_engine.interpret_goal(goal)
        return self.reasoning_engine.create_plan(interpreted["objective"])
