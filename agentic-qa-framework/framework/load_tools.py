import os
import sys
import importlib
import inspect

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

ACTIONS_DIR = os.path.join(BASE_DIR, "framework", "actions")


def load_tools():

    tools = {}

    for file in os.listdir(ACTIONS_DIR):

        if not file.endswith(".py") or file == "__init__.py":
            continue

        module_name = file.replace(".py", "")
        module_path = f"framework.actions.{module_name}"

        module = importlib.import_module(module_path)

        for name, func in inspect.getmembers(module, inspect.isfunction):
            tools[name] = func
            print("Loaded tool:", name)

    return tools


if __name__ == "__main__":
    print(load_tools())