from __future__ import annotations

from browser.browser_controller import BrowserController
from utils.helpers import GeneratedTest


class TestExecutor:
    def __init__(self, browser: BrowserController) -> None:
        self.browser = browser

    def execute(self, test: GeneratedTest) -> dict:
        # Future work: map generated graph steps back to semantic DOM candidates.
        return {
            "name": test.name,
            "status": "not_implemented",
            "steps": test.steps,
            "expected_result": test.expected_result,
        }
