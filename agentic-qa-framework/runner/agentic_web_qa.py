import json
import os
import sys

import requests
import numpy as np
import torch

from playwright.sync_api import sync_playwright
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from framework.load_tools import load_tools
import inspect
from agent.golden_prompts import PromptBuilder
from agent.rag_memory import RAGMemory
from config.model_config import MODEL_CONFIG
import re
# from agent.automation_agent import execute_action
from agent.react_pipeline import ReactPipeline

############################################################
# CONFIG
############################################################

LOGIN_URL = "https://zodiacappqp.zv8.zodiac-cloud.com/zodiac/ui/auth"

USERNAME = "username"
PASSWORD = "password"

OLLAMA_URL = "http://localhost:11434/api/generate"
# OLLAMA_MODEL = "llama3.1:8b"
# OLLAMA_MODEL = "qwen2.5:7b"
# OLLAMA_MODEL = "deepseek-coder:6.7b"

MAX_STEPS = 25

############################################################
# VECTOR MEMORY
############################################################

class VectorMemory:

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
    device=device
        )

        self.data = []

    def add(self, text, metadata):

        emb = self.model.encode(text)

        self.data.append({
            "embedding": emb,
            "text": text,
            "metadata": metadata
        })

    def search(self, query, k=3):

        if not self.data:
            return []

        q = self.model.encode(query)

        scores = []

        for item in self.data:

            sim = float(np.dot(q, item["embedding"]))

            scores.append({
                "score": sim,
                "item": item
            })

        scores = sorted(scores, key=lambda x: x["score"], reverse=True)

        return [x["item"] for x in scores[:k]]


############################################################
# BROWSER CONTROLLER
############################################################

class BrowserController:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context(
            ignore_https_errors=True
        )

        self.page = self.context.new_page()

    def open(self, url):

        print("Opening:", url)

        self.page.goto(url)

        self.page.wait_for_timeout(4000)

    ########################################################
    def click(self, text):

        print("CLICK:", text)

        try:

            btn = self.page.get_by_role("button", name=text)

            if btn.count() > 0:
                btn.first.click()

                return True

        except:
            pass

        try:

            btn = self.page.locator(f"button:has-text('{text}')")

            if btn.count() > 0:
                btn.first.click()

                return True

        except:
            pass

        return False

    ########################################################
    def fill(self, field, value):

        print("FILL:", field)

        try:

            loc = self.page.locator(field)

            if loc.count() > 0:
                loc.first.fill(value)

                return True

        except Exception as e:

            print("Fill failed:", e)

        return False

    ########################################################
    def extract_dom(self):

        elements = self.page.evaluate("""
                                      () => {

                                          function visible(el) {
                                              const r = el.getBoundingClientRect();
                                              return r.width > 0 && r.height > 0;
                                          }

                                          function identifier(el) {
                                              return (
                                                  el.innerText ||
                                                  el.id ||
                                                  el.name ||
                                                  el.placeholder ||
                                                  el.getAttribute("aria-label") ||
                                                  ""
                                              ).trim()
                                          }

                                          const nodes = []

                                          const selectors = `
                button,
                input,
                select,
                textarea,
                a,
                [role="button"]
            `

                                          document.querySelectorAll(selectors).forEach(el => {

                                              if (!visible(el)) return

                                              const id = identifier(el)

                                              if (!id) return

                                              nodes.push({

                                                  tag: el.tagName.toLowerCase(),
                                                  text: (el.innerText || "").trim(),
                                                  id: el.id || "",
                                                  name: el.name || "",
                                                  placeholder: el.placeholder || "",
                                                  role: el.getAttribute("role") || "",
                                                  type: el.type || ""

                                              })

                                          })

                                          return nodes

                                      }
                                      """)

        return elements

############################################################
# LLM CLIENT
############################################################
class OllamaClient:
    def generate(self, prompt, config):

        payload = {
            "model": config["model"],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config.get("temperature", 0)
            },
            "format": "json"
        }

        for attempt in range(2):
            try:
                r = requests.post(OLLAMA_URL, json=payload, timeout=60)
                r.raise_for_status()

                data = r.json()
                text = data.get("response", "")

                try:
                    return json.loads(text)
                except:
                    match = re.search(r'\{[\s\S]*\}', text)
                    if match:
                        return json.loads(match.group())

                return {}

            except Exception as e:
                print(f"❌ LLM call failed (attempt {attempt + 1}):", e)

        return {}



def clean_url(url):

    if not url:
        return url

    # remove LLM tokens
    url = re.sub(r"<.*?>", "", url)

    # remove tokenizer artifacts
    url = url.replace("▁", "")

    return url.strip()
############################################################
# ACTION EXECUTOR
############################################################
class ActionExecutor:

    def __init__(self, browser, tools):

        self.browser = browser
        self.page = browser.page
        self.tools = tools

    def execute(self, action):

        action_type = action.get("action_type")
        selector = action.get("selector")
        value = action.get("value") or action.get("target_text")
        target_url = action.get("target_url")

        if not action_type:
            print("Invalid action from LLM")
            return False

        action_type = action_type.lower().strip()

        if action_type not in self.tools:
            print("Invalid tool:", action_type)
            return False

        tool = self.tools[action_type]
        if not self.validate_tool_inputs(action, tool):
            return False
        try:

            if action_type == "open_url":
                tool(self.page, clean_url(target_url))

            elif action_type == "click":
                tool(self.page, selector)

            elif action_type == "hover":
                tool(self.page, selector)

            elif action_type == "assert_visible":
                tool(self.page, selector)

            elif action_type == "fill_input":
                tool(self.page, selector, value)

            elif action_type == "clear_input":
                tool(self.page, selector)

            elif action_type == "go_back":
                tool(self.page)

            elif action_type == "refresh":
                tool(self.page)

            else:
                print("Unhandled tool:", action_type)
                return False

            return True


        except Exception as e:

            print(f"❌ Tool failed | action={action_type} | selector={selector} | value={value} | error={e}")

            return False

    def validate_tool_inputs(self, action, tool):

        sig = inspect.signature(tool)
        params = list(sig.parameters.keys())

        # remove 'page'
        params = [p for p in params if p != "page"]

        selector = action.get("selector")
        value = action.get("value") or action.get("target_text")
        target_url = action.get("target_url")

        for p in params:

            if p == "selector":
                if not selector:
                    print("❌ Missing selector")
                    return False

            elif p == "url":
                if not target_url:
                    print("❌ Missing URL")
                    return False

            else:
                # any other param = treat as value
                if not value:
                    print(f"❌ Missing value for param: {p}")
                    return False

        return True
############################################################
# AGENT
############################################################

class WebAgent:

    def __init__(self):

        self.browser = BrowserController()

        self.llm = OllamaClient()

        self.rag_memory = RAGMemory()

        self.rag_memory.setup_rag()

        self.tools = load_tools()

        self.executor = ActionExecutor(
            self.browser,
            self.tools
        )
        self.react_pipeline = ReactPipeline(
            self.browser,
            self.llm,
            self.executor,
            self.tools,
            self.rag_memory
        )

        self.history = []

    ########################################################
    def run(self, goal):

        ##################################################
        # OPEN APPLICATION
        ##################################################

        self.browser.open(LOGIN_URL)



        print("\nPLANNING TASK\n")
        ##################################################
        # RAG MEMORY SEARCH
        ##################################################

        results = self.rag_memory.search(goal, k=3)

        memory_context = results  # 🔥 keep full RAG objects

        print("\nRAG CONTEXT")
        print(memory_context)

        ##################################################
        # PLANNER
        ##################################################

        plan_data = self.llm.generate(
            PromptBuilder.planner(
                goal,
                memory_context
            ),
            MODEL_CONFIG["planner"]
        )

        plan = plan_data.get("plan", [])
        if not plan:
            print("❌ Planner failed to generate plan")
            return

        print("\nPLAN")
        for step in plan:
            print("PLAN STEP:", step)

        ##################################################
        # EXECUTE PLAN USING REACT PIPELINE
        ##################################################

        print("\nSTARTING REACT PIPELINE\n")

        self.react_pipeline.execute_plan(
            goal,
            plan,
            self.rag_memory
        )

        ##################################################
        # FINAL STATUS
        ##################################################

        if "dashboard" in self.browser.page.url.lower():

            print("\nLOGIN SUCCESS")

        else:

            print("\nAGENT FINISHED BUT LOGIN NOT DETECTED")
############################################################
# MAIN
############################################################

if __name__ == "__main__":

    goal = "open zodiac application and see login page, enter username and password and click login to application and verify"

    agent = WebAgent()

    agent.run(goal)