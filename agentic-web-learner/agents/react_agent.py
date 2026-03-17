from __future__ import annotations

from engine.llm_reasoning_engine import LLMReasoningEngine
from utils.helpers import ReactStep


class ReactAgent:
    """ReAct agent whose decisions come entirely from the local Ollama model."""

    def __init__(self, reasoning_engine: LLMReasoningEngine) -> None:
        self.reasoning_engine = reasoning_engine

    def decide_next_action(
        self,
        goal: str,
        page_summary: dict,
        visited_actions: list[str],
        rag_context: dict,
        source_page: str,
    ) -> ReactStep:
        decision = self.reasoning_engine.decide_step(goal, page_summary, rag_context, visited_actions)
        action = self.reasoning_engine.build_action(decision, source_page)
        thought = decision.get("thought", "")
        if isinstance(thought, dict):
            thought = thought.get("objective") or thought.get("thought") or str(thought)
        return ReactStep(thought=str(thought), action=action, observation="")
