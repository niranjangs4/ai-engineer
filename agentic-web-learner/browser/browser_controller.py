from __future__ import annotations

import time
from dataclasses import asdict
from pathlib import Path
from typing import Callable, TypeVar

from playwright.sync_api import Browser, BrowserContext, Error, Page, TimeoutError, sync_playwright

from config.settings import Settings
from utils.helpers import BrowserAction, ensure_directory
from utils.logger import configure_logging, log_block


T = TypeVar("T")


class BrowserController:
    """Playwright wrapper exposing semantic browser tools to the agent."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.logger = configure_logging(settings.log_level)
        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=settings.headless)
        self.context: BrowserContext = self.browser.new_context(ignore_https_errors=True)
        self.page: Page = self.context.new_page()
        self.page.set_default_timeout(settings.browser_timeout_ms)

    def open_url(self, url: str) -> None:
        log_block(self.logger, "TOOL EXECUTION", f'open_url("{url}")')
        self._retry(lambda: self.page.goto(url, wait_until="domcontentloaded", timeout=self.settings.browser_timeout_ms))
        self.wait_for_page_ready()
        log_block(self.logger, "TOOL RESULT", f"Opened URL successfully: {self.current_url()}")

    def execute_action(self, action: BrowserAction) -> bool:
        try:
            target = action.target_text or action.text or action.value or ""
            payload = asdict(action)
            if payload.get("value"):
                payload["value"] = "***MASKED***" if action.action_type == "fill" else payload["value"]
            log_block(self.logger, "TOOL INPUT PAYLOAD", str(payload))
            log_block(self.logger, "TOOL EXECUTION", f"{action.action_type}({target})")
            if action.action_type == "click":
                self.click_element(action.target_text or action.text)
            elif action.action_type == "fill":
                self.fill_input(action.target_text or action.text, action.value or "")
            elif action.action_type == "navigate_back":
                self.navigate_back()
            elif action.action_type == "scroll_page":
                self.scroll_page(action.value or "down")
            elif action.action_type == "open_url" and action.value:
                self.open_url(action.value)
            elif action.action_type == "capture_screenshot" and action.value:
                self.capture_screenshot(action.value)
            else:
                raise ValueError(f"Unsupported action type: {action.action_type}")
            log_block(self.logger, "TOOL RESULT", f"Action completed successfully: {action.action_type}")
            return True
        except Exception as exc:
            log_block(self.logger, "TOOL ERROR", f"Action failed for target '{action.target_text or action.text}': {exc}")
            return False

    def click_element(self, element_text: str) -> None:
        def operation() -> None:
            clicked = self.page.evaluate(
                """
                (targetText) => {
                    const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim().toLowerCase();
                    const target = normalize(targetText);
                    const nodes = Array.from(document.querySelectorAll('button, a, [role="button"], [role="menuitem"], [role="tab"], input[type="button"], input[type="submit"], [onclick]'));
                    for (const node of nodes) {
                        const text = normalize(node.innerText || node.textContent || node.getAttribute('aria-label') || node.value || '');
                        if (!text) continue;
                        if (text === target || text.includes(target) || target.includes(text)) {
                            node.click();
                            return true;
                        }
                    }
                    return false;
                }
                """,
                element_text,
            )
            if not clicked:
                raise RuntimeError(f"No clickable element found for text '{element_text}'.")
            self.wait_for_page_ready()

        self._retry(operation)

    def fill_input(self, field_text: str, value: str) -> None:
        def operation() -> None:
            filled = self.page.evaluate(
                """
                ({ fieldText, value }) => {
                    const normalize = (input) => (input || '').replace(/\\s+/g, ' ').trim().toLowerCase();
                    const target = normalize(fieldText);
                    const inputs = Array.from(document.querySelectorAll('input, textarea'));
                    for (const node of inputs) {
                        const id = node.getAttribute('id');
                        let label = '';
                        if (id) {
                            const labels = Array.from(document.querySelectorAll('label')).filter(labelNode => labelNode.getAttribute('for') === id);
                            if (labels.length > 0) label = labels[0].innerText || labels[0].textContent || '';
                        }
                        if (!label) {
                            const parentLabel = node.closest('label');
                            if (parentLabel) label = parentLabel.innerText || parentLabel.textContent || '';
                        }
                        const candidates = [
                            node.getAttribute('placeholder') || '',
                            node.getAttribute('name') || '',
                            node.getAttribute('aria-label') || '',
                            label,
                            node.type || '',
                            node.innerText || '',
                            node.textContent || '',
                        ].map(normalize);
                        if (candidates.some(candidate => candidate && (candidate === target || candidate.includes(target) || target.includes(candidate)))) {
                            node.focus();
                            if ('value' in node) {
                                node.value = value;
                            } else {
                                node.textContent = value;
                            }
                            node.dispatchEvent(new Event('input', { bubbles: true }));
                            node.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                    }
                    return false;
                }
                """,
                {"fieldText": field_text, "value": value},
            )
            if not filled:
                raise RuntimeError(f"No input field found for text '{field_text}'.")

        self._retry(operation)
        log_block(self.logger, "TOOL RESULT", f"Filled input successfully: {field_text}")

    def navigate_back(self) -> None:
        log_block(self.logger, "TOOL EXECUTION", 'navigate_back()')
        self.page.go_back(wait_until="domcontentloaded", timeout=self.settings.browser_timeout_ms)
        self.wait_for_page_ready()
        log_block(self.logger, "TOOL RESULT", f"Navigated back to: {self.current_url()}")

    def scroll_page(self, direction: str = "down") -> None:
        log_block(self.logger, "TOOL EXECUTION", f'scroll_page("{direction}")')
        amount = 700 if direction.lower() == "down" else -700
        self.page.evaluate("(pixels) => window.scrollBy(0, pixels)", amount)
        self.page.wait_for_timeout(500)
        log_block(self.logger, "TOOL RESULT", f"Scrolled page: {direction}")

    def extract_dom(self) -> str:
        return self.page.content()

    def save_dom_snapshot(self, output_path: str) -> None:
        output = Path(output_path)
        ensure_directory(output.parent)
        output.write_text(self.extract_dom(), encoding="utf-8")
        log_block(self.logger, "DOM SNAPSHOT", str(output))

    def capture_screenshot(self, output_path: str) -> None:
        output = Path(output_path)
        ensure_directory(output.parent)
        self.page.screenshot(path=str(output), full_page=True)
        log_block(self.logger, "SCREENSHOT", str(output))

    def current_url(self) -> str:
        return self.page.url

    def title(self) -> str:
        try:
            return self.page.title()
        except Error:
            return ""

    def visible_text(self) -> str:
        try:
            return self.page.evaluate("() => document.body ? (document.body.innerText || '') : ''")
        except Exception:
            return ""

    def wait_for_page_ready(self) -> None:
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=self.settings.browser_timeout_ms)
            self.page.wait_for_load_state("networkidle", timeout=min(self.settings.browser_timeout_ms, 5000))
        except TimeoutError:
            self.logger.warning("Page did not reach network idle before timeout; continuing with current DOM.")

    def close(self) -> None:
        try:
            self.context.close()
            self.browser.close()
        finally:
            self.playwright.stop()

    def _retry(self, operation: Callable[[], T]) -> T:
        attempt = 0
        last_error: Exception | None = None
        while attempt <= self.settings.max_retries:
            try:
                return operation()
            except (TimeoutError, Error, RuntimeError) as exc:
                last_error = exc
                attempt += 1
                self.logger.warning(
                    "Browser operation failed on attempt %s/%s: %s",
                    attempt,
                    self.settings.max_retries + 1,
                    exc,
                )
                time.sleep(1)
        raise RuntimeError(f"Browser operation failed after retries: {last_error}") from last_error
