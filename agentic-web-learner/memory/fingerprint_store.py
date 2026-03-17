from __future__ import annotations

from dataclasses import dataclass

from utils.helpers import UIElement, stable_hash


@dataclass(slots=True)
class ElementFingerprint:
    fingerprint_id: str
    text: str
    element_type: str
    container: str
    neighboring_elements: tuple[str, ...]
    clickable: bool
    candidate_id: str
    page_url: str | None


class FingerprintStore:
    """Stores resilient UI fingerprints for self-healing and recall."""

    def __init__(self) -> None:
        self._fingerprints: dict[str, ElementFingerprint] = {}

    def store(self, element: UIElement) -> ElementFingerprint:
        fingerprint = ElementFingerprint(
            fingerprint_id=stable_hash(
                {
                    "text": element.text,
                    "type": element.element_type,
                    "container": element.container,
                    "neighbors": element.neighboring_elements,
                    "clickable": element.clickable,
                }
            ),
            text=element.text,
            element_type=element.element_type,
            container=element.container,
            neighboring_elements=tuple(element.neighboring_elements),
            clickable=element.clickable,
            candidate_id=element.candidate_id,
            page_url=element.page_url,
        )
        self._fingerprints[fingerprint.fingerprint_id] = fingerprint
        return fingerprint

    def get(self, fingerprint_id: str) -> ElementFingerprint | None:
        return self._fingerprints.get(fingerprint_id)

    def find_similar(self, text: str, element_type: str | None = None) -> list[ElementFingerprint]:
        results: list[ElementFingerprint] = []
        for fingerprint in self._fingerprints.values():
            if text.lower() in fingerprint.text.lower():
                if element_type is None or element_type == fingerprint.element_type:
                    results.append(fingerprint)
        return results
