from __future__ import annotations

from utils.helpers import BrowserAction, FailureReport, PageStateSignature


class StateManager:
    """Tracks visited pages, actions, failures, and current exploration progress."""

    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth
        self.visited_pages: dict[str, PageStateSignature] = {}
        self.visited_action_ids: set[str] = set()
        self.failed_action_ids: set[str] = set()
        self.current_page: PageStateSignature | None = None
        self.exploration_depth: int = 0
        self.failure_reports: list[FailureReport] = []

    def set_current_page(self, state: PageStateSignature) -> None:
        self.current_page = state
        self.visited_pages[state.id] = state

    def mark_action_visited(self, action: BrowserAction) -> None:
        self.visited_action_ids.add(action.action_id)
        self.exploration_depth = max(self.exploration_depth, action.depth)

    def mark_action_failed(self, action: BrowserAction) -> None:
        self.failed_action_ids.add(action.action_id)

    def has_seen_action(self, action: BrowserAction) -> bool:
        return action.action_id in self.visited_action_ids or action.action_id in self.failed_action_ids

    def has_seen_page(self, state: PageStateSignature) -> bool:
        return state.id in self.visited_pages

    def can_explore(self, action: BrowserAction) -> bool:
        return action.depth <= self.max_depth and not self.has_seen_action(action)

    def record_failure(self, report: FailureReport) -> None:
        self.failure_reports.append(report)
