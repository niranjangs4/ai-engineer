from __future__ import annotations


class ElementDetector:
    """Shared heuristic helpers for semantic UI classification."""

    def detect_type(self, tag_name: str, role: str, classes: str, text: str, input_type: str) -> str:
        tag_name = tag_name.lower()
        role = role.lower()
        classes = classes.lower()
        text = text.lower()
        input_type = input_type.lower()

        if tag_name in {"input", "textarea"} or role == "textbox":
            return "input"
        if tag_name == "button" or role == "button" or "btn" in classes:
            return "button"
        if role == "tab" or "tab" in classes:
            return "tab"
        if role == "menuitem" or "menu" in classes or "nav" in classes:
            return "menu"
        if tag_name == "a" or "link" in classes:
            return "link"
        if input_type == "password":
            return "input"
        if "login" in text or "sign in" in text:
            return "button"
        return "link"
