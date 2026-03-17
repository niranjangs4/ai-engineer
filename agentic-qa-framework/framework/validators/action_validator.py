def validate_action(action, tools, dom=None, rag_memory=None):

    action_type = action.get("action_type")

    if not action_type:
        print("Invalid action: missing action_type")
        return False

    if action_type == "done":
        return True

    if action_type not in tools:
        print(f"Invalid tool from LLM: {action_type}")
        return False
    selector = action.get("selector")

    if selector:
        selector = selector.strip()

    if selector and dom:

        dom_selectors = [
            el.get("selector") for el in dom if el.get("selector")
        ]

        rag_selectors = []

        if rag_memory:
            for item in rag_memory:
                if not isinstance(item, dict):
                    continue

                meta = item.get("metadata")

                if not meta:
                    continue

                if meta.get("type") == "selector" and meta.get("selector"):
                    rag_selectors.append(meta.get("selector"))

        valid_selectors = set(dom_selectors + rag_selectors)

        if selector not in valid_selectors:
            print(f"Invalid selector: {selector}")
            return False
    return True