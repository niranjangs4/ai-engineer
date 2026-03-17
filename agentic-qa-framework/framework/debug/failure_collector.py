import json
import os
from datetime import datetime


class FailureCollector:

    def __init__(self, page):
        self.page = page

    def collect(self, plan, current_step, dom):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        os.makedirs("logs", exist_ok=True)

        screenshot_path = f"logs/failure_{timestamp}.png"
        json_path = f"logs/failure_{timestamp}.json"

        # Take screenshot
        self.page.screenshot(path=screenshot_path)

        completed = []
        remaining = []

        for step in plan:
            if step["done"]:
                completed.append(step["action"])
            else:
                remaining.append(step["action"])

        data = {
            "timestamp": timestamp,
            "url": self.page.url,
            "page_title": self.page.title(),

            "failed_step": current_step["action"],

            "completed_steps": completed,
            "remaining_steps": remaining,

            "plan": plan,

            "visible_dom": dom,

            "screenshot": screenshot_path
        }

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        print("\nFailure evidence saved:")
        print(json_path)

        return screenshot_path, json_path