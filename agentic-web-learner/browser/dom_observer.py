from __future__ import annotations

from browser.dom_extractor import DOMExtractor
from browser.dom_summarizer import DOMSummarizer
from utils.helpers import UIElement


class DOMObserver:
    """Coordinates live DOM extraction and summarization for the reasoning loop."""

    def __init__(self) -> None:
        self.extractor = DOMExtractor()
        self.summarizer = DOMSummarizer()

    def observe(self, page, page_url: str, title: str) -> tuple[list[UIElement], dict]:
        elements = self.extractor.extract(page, page_url)
        summary = self.summarizer.summarize(page_url, title, elements)
        return elements, summary
