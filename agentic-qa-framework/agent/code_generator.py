import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
from config.model_config import MODEL_CONFIG


MODEL = MODEL_CONFIG["code_generator"]["model"]
TEMP = MODEL_CONFIG["code_generator"]["temperature"]


def generate_method(method_name):
    prompt = f"""
    You are a senior Python Playwright automation engineer.

    Generate ONLY a Python function.

    Function name: {method_name}

    The function must be compatible with a Playwright automation framework
    where the browser and page are already created.

    General Rules:

    1. The first parameter must always be `page`.
    2. Infer the required parameters from the function name.

    Generate ONLY a Python function.

    Requirements:
    - Use Playwright sync API
    - Function name: {method_name}
    - Do NOT import playwright
    - Do NOT create browser
    - Do NOT add explanation
    - Do NOT use markdown
    - Output ONLY valid Python code

    Typical patterns:

    Navigation actions
    - open / navigate
    → use page.goto(url)
    parameters = (page, url)

    Click actions
    - click / press / tap
    → use page.click(selector)
    parameters = (page, selector)

    Input actions
    - fill / type / enter
    → use page.fill(selector, value)
    parameters = (page, selector, value)

    Select actions
    - select / choose
    → use page.select_option(selector, value)

    Wait actions
    - wait
    → use page.wait_for_selector(selector)

    3. Do NOT create browser or playwright instance.

    4. Do NOT import playwright.

    5. Output ONLY valid Python code.

    Example outputs:

    def click_button(page, selector):
        page.click(selector)

    def open_page(page, url):
        page.goto(url)

    def fill_username(page, selector, value):
        page.fill(selector, value)
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMP
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        raw_output = response.json().get("response", "")
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return None

    # clean the output
    try:
        clean_code = extract_function(raw_output)
    except Exception as e:
        print(f"❌ Function extraction failed: {e}")
        return None
    return clean_code

def extract_function(llm_output):

    # remove markdown
    llm_output = llm_output.replace("```python", "")
    llm_output = llm_output.replace("```", "")

    lines = llm_output.split("\n")

    start = None

    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            start = i
            break

    if start is None:
        raise Exception("No function found in LLM output")

    function_code = "\n".join(lines[start:]).strip()

    return function_code