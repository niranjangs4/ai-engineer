import base64
import json
import requests
# from PIL import Image

OLLAMA_URL = "http://localhost:11434/api/generate"
from config.model_config import MODEL_CONFIG


MODEL = MODEL_CONFIG["vision"]["model"]
TEMP = MODEL_CONFIG["vision"]["temperature"]


def encode_image(image_path):

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# analysis = analyze_ui(screenshot_path, self.plan, self.current_step)


def analyze_ui(image_path, plan, current_step):

    # image_path = r"C:\Users\niran\PycharmProjects\ai-engineer\agentic-qa-framework\agent\img.png"

    image_base64 = encode_image(image_path)
    prompt = f"""
    You are a senior QA automation engineer with 30+ years of experience in testing enterprise web applications.

    Your task is to carefully inspect the provided screenshot of a web application and perform a deep UI analysis exactly as an experienced QA engineer would do.
    
    IMPORTANT
    You must carefully scan the entire screenshot from top to bottom and left to right and identify every visible detail.
    
    Do NOT miss any text, labels, error messages, warnings, dialogs, popups, buttons, menus, or UI components.
    
    If any error message or warning appears anywhere in the UI, it must be detected and reported.
    
    VERSION DETECTION
    Look for version numbers such as:
    - v1.2.3
    - 8.0.0 r160h9
    - Build 1234
    - Release numbers
    - UI build numbers
    
    ERROR DETECTION Carefully analyze the screenshot and give me report
    
    
    ------------------------------------------------
    IMPORTANT ERROR RULES
    ------------------------------------------------
    
    Only mark error_detected=true if it blocks the current step.    
    
    If any of these words appear in the screenshot, set:
    
    Set "error_detected": true if visible UI contains critical failure indicators like:
    - error
    - failed
    - exception
    - not found
    - invalid
    - server error
    - 404
    - 500
    
    AND it blocks the current step → set "error_detected": true
    
     PLANNED STEPS:
     {json.dumps(plan, indent=2)}
    
    Current Failed Step:
    {json.dumps(current_step, indent=2)}
    
    ------------------------------------------------
    OUTPUT FORMAT
    ------------------------------------------------
    
    Return ONLY valid JSON.
    
    {{
      "application": "",
      "environment": "",
      "module": "",
      "page": "",
      "url": "",
      "version_detected": "",
      "visible_text": [],
      "error_detected": true/false,
      "error_type": "",
      "error_summary": "",
      "possible_root_cause": "",
      "automation_suggestion": "",
      "bug_report": {{
        "title": "",
        "module": "",
        "page": "",
        "environment": "",
        "url": "",
        "description": "",
        "steps_to_reproduce": [],
        "expected_result": "",
        "actual_result": "",
        "severity": ""
      }}
    }}
    
    Return raw JSON only.
    
    Do NOT include explanations.
    Do NOT use markdown.
    Do NOT include extra text.
    """
    print(prompt)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "options": {
            "temperature": TEMP
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        raw = response.json().get("response", "")
    except Exception as e:
        print("❌ Vision API failed:", e)
        return {"error_detected": True, "error": str(e)}

    # 🔥 CLEAN MARKDOWN
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except:
        print("⚠️ Failed to parse vision output, returning raw")
        return {"error_detected": True, "raw_output": raw}


# if __name__ == "__main__":
#
#     screenshot = "error_screen.png"
#
#     print("\nAnalyzing screenshot using qwen2.5vl:7b...\n")
#
#     result = analyze_ui(screenshot)
#
#     print(json.dumps(result, indent=2))