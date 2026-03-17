import copy
import json
from enum import Enum


from agent.golden_prompts import PromptBuilder
from framework.debug.failure_collector import FailureCollector
from framework.validators.action_validator import validate_action
from agent.vision_agent import analyze_ui
from config.model_config import MODEL_CONFIG


class ReactState(Enum):

    START = "start"
    THOUGHT = "thought"
    ACTION = "action"
    EXECUTE = "execute"
    OBSERVE = "observe"
    EVALUATE = "evaluate"
    DONE = "done"


class ReactPipeline:

    def __init__(self, browser, llm, executor, tools, rag_memory):
        self.browser = browser
        self.rag_memory = rag_memory
        self.llm = llm
        self.executor = executor
        self.tools = tools
        self.history = []
        self.state = ReactState.START

        self.observation = "None"
        self.last_decision = None

        self.plan = []
        self.current_step = None

    ########################################################
    def heal_selector(self, selector, dom):

        if not selector:
            return selector

        selector_lower = selector.lower()

        best_match = None

        for el in dom:
            text = (el.get("text") or "").lower()

            if not text:
                continue

            # score based match
            score = 0

            if selector_lower == text:
                return el.get("selector")

            elif selector_lower in text:
                score = 2

            elif all(word in text for word in selector_lower.split()):
                score = 1

            if score > 0:
                best_match = el.get("selector")

        return best_match if best_match else (selector or "")


    def execute_plan(self, goal, plan, rag_memory):

        self.history = []
        self.plan = plan

        for step in plan:

            self.current_step = step

            print("\n==============================")
            print("EXECUTING PLAN STEP:", step)
            print("==============================")

            self.state = ReactState.START
            self.observation = "None"
            self.react_cycle(goal, step["action"], rag_memory)

            if self.observation == "Action executed successfully":
                # step["done"] = True
                if "successfully" in self.observation:
                    step["done"] = True
                    step["status"] = "passed"
                else:
                    step["done"] = False
                    step["status"] = "failed"

    ########################################################

    def react_cycle(self, goal, plan_step, rag_memory):

        loop_guard = 0
        self.retry_count = 0  # ✅ reset per step

        while self.state != ReactState.DONE:

            if loop_guard > 10:
                print("❌ React loop exceeded limit — marking step failed")
                self.observation = "Step failed after multiple attempts"
                self.state = ReactState.DONE
                break

            print("\nCURRENT STATE:", self.state.value)

            if self.state == ReactState.START:

                self.state = ReactState.THOUGHT

            ################################################

            elif self.state == ReactState.THOUGHT:

                dom = self.browser.extract_dom()

                # optimizer_prompt = PromptBuilder.build_semantic_dom(dom)
                # print("optimizer_prompt")
                # print(optimizer_prompt)
                optimized_dom = PromptBuilder.build_semantic_dom(dom)
                prompt = PromptBuilder.react(
                    goal,
                    plan_step,
                    optimized_dom,
                    self.observation,
                    rag_memory,
                    self.history[-5:],
                    self.tools
                )
                print("React prompt:",plan_step)
                # print(prompt)
                print("\n🧠 THOUGHT PROMPT")

                decision = self.llm.generate(
                    prompt,
                    MODEL_CONFIG["executor"]
                )

                # 🔥 VALIDATE BEFORE USING
                if not isinstance(decision, dict):
                    print("❌ Invalid LLM output format:", decision)

                    self.observation = "Invalid LLM response format"
                    self.retry_count += 1

                    if self.retry_count < 2:
                        self.state = ReactState.THOUGHT
                        continue

                    self.state = ReactState.DONE
                    continue

                if "action_type" not in decision:
                    print("❌ Missing action_type in LLM response")

                    self.observation = "LLM response missing action_type"
                    self.retry_count += 1

                    if self.retry_count < 2:
                        self.state = ReactState.THOUGHT
                        continue

                    self.state = ReactState.DONE
                    continue

                # ✅ ONLY NOW assign
                self.last_decision = decision

                print("🧠 DECISION:", json.dumps(decision, indent=2))

                self.state = ReactState.ACTION

            ################################################

            elif self.state == ReactState.ACTION:

                # 🔥 FIX 3: validate LLM response before using it

                if not self.last_decision or "action_type" not in self.last_decision:

                    print("❌ Invalid LLM response:", self.last_decision)

                    self.observation = "Invalid LLM response"

                    self.retry_count += 1

                    if self.retry_count < 2:
                        print("🔁 Retrying due to invalid LLM output...")

                        self.state = ReactState.THOUGHT

                        continue

                    print("❌ LLM failed multiple times — stopping step")

                    self.state = ReactState.DONE

                    continue

                action = self.last_decision.get("action_type")

                print("⚙️ ACTION:", action)

                if action == "done":

                    self.state = ReactState.DONE


                else:

                    self.state = ReactState.EXECUTE

            ################################################

            elif self.state == ReactState.EXECUTE:

                dom = self.browser.extract_dom()
                optimized_dom = PromptBuilder.build_semantic_dom(dom)

                # 🔥 STEP 1: Capture original LLM selector
                original_selector = self.last_decision.get("selector")

                learned_selector = None
                used_rag = False

                # 🔥 STEP 2: Try RAG selector first
                rag_results = self.rag_memory.search(self.current_step["action"], k=3)

                for item in rag_results:

                    meta = item.get("metadata", item)

                    step_action = self.current_step["action"].lower().replace(" ", "_")
                    meta_action = meta.get("action")

                    if not meta_action:
                        continue

                    meta_action = meta_action.lower()

                    step_words = set(step_action.split("_"))
                    meta_words = set(meta_action.split("_"))

                    if step_words & meta_words:
                        learned_selector = meta.get("selector")

                        print(f"🧠 Using learned selector: {learned_selector}")

                        used_rag = True
                        break

                # 🔥 STEP 3: Heal selector (RAG or LLM)
                current_selector = self.last_decision.get("selector")

                healed = self.heal_selector(current_selector, optimized_dom)
                healed_changed = current_selector != healed

                if healed_changed:
                    print(f"🩹 Selector healed: {current_selector} → {healed}")
                self.last_decision["selector"] = healed

                # ✅ FINAL SELECTOR CHECK (CORRECT PLACE)
                if not self.last_decision.get("selector") and self.last_decision.get("action_type") not in [
                    "open_url", "go_back", "refresh"
                ]:
                    print("❌ Missing selector before execution")
                    self.state = ReactState.THOUGHT
                    continue
                # 🔥 STEP 5: Execute (RAG or LLM selector)
                candidate_selectors = []

                # 1. RAG selector (highest priority)
                if learned_selector:
                    candidate_selectors.append(learned_selector)

                # 2. Original LLM selector
                if original_selector and original_selector not in candidate_selectors:
                    candidate_selectors.append(original_selector)

                # 3. Healed selector
                healed_selector = self.last_decision.get("selector")
                if healed_selector and healed_selector not in candidate_selectors:
                    candidate_selectors.append(healed_selector)
                # ✅ ADD THIS BLOCK HERE
                candidate_selectors = [s for s in candidate_selectors if s]

                if not candidate_selectors:
                    print("❌ No valid selectors to try")

                    self.observation = "No valid selector found"
                    self.retry_count += 1

                    if self.retry_count < 2:
                        self.state = ReactState.THOUGHT
                        continue

                    self.state = ReactState.EVALUATE
                    continue

                # ✅ 👉 ADD HERE (IMPORTANT LOCATION)
                # ✅ REPEAT DETECTION (UPGRADED)
                # ✅ REPEAT DETECTION (FINAL SAFE VERSION)
                recent = self.history[-3:] if self.history else []

                repeat_detected = False

                for h in recent:
                    prev_action = h.get("action", {})
                    prev_selector = prev_action.get("selector")
                    prev_type = prev_action.get("action_type")

                    if not prev_selector or not prev_type:
                        continue

                    if prev_type == self.last_decision.get("action_type") and \
                            prev_selector in candidate_selectors:
                        repeat_detected = True
                        break

                if repeat_detected:
                    print("⚠️ Repeating recent action — forcing rethink")

                    self.observation = "Repeated action detected. Use a DIFFERENT selector from UI elements."

                    # 🔥 force stronger retry signal
                    self.retry_count += 1

                    self.state = ReactState.THOUGHT
                    continue


                # 🔽 EXISTING CODE CONTINUES
                success = False
                for sel in candidate_selectors:

                    action_copy = copy.deepcopy(self.last_decision)
                    action_copy["selector"] = sel

                    if not validate_action(action_copy, self.tools, optimized_dom, self.rag_memory.data):
                        print(f"⚠️ Skipping invalid selector: {sel}")
                        continue

                    print(f"🔄 Trying selector: {sel}")

                    if self.executor.execute(action_copy):
                        success = True
                        self.last_decision = action_copy
                        break

                # 🔥 STEP 6: FALLBACK LOGIC (THIS IS THE KEY ADDITION)
                if not success and used_rag and original_selector:
                    print("🔁 RAG selector failed → falling back to LLM selector")

                    fallback_action = copy.deepcopy(self.last_decision)

                    fallback_action["selector"] = self.last_decision.get("selector") or original_selector
                    success = self.executor.execute(fallback_action)

                    if success:
                        self.last_decision = fallback_action
                if success:

                    self.observation = "Action executed successfully"
                    self.retry_count = 0

                    # ✅ ADD HISTORY HERE
                    self.history.append({
                        "step": self.current_step["action"],
                        "action": copy.deepcopy(self.last_decision),  # ✅ FIX
                        "result": self.observation
                    })

                    # limit history
                    if len(self.history) > 5:
                        self.history = self.history[-5:]

                    final_selector = self.last_decision.get("selector")

                    if used_rag:
                        print("📈 Reinforcing RAG selector confidence")
                        self.rag_memory.add(
                            text=f"{self.current_step['action']} selector reinforcement",
                            metadata={
                                "type": "selector",
                                "application": "zodiac",
                                "page": self.browser.page.url,
                                "action": self.current_step["action"],
                                "selector": final_selector
                            }
                        )

                    elif final_selector and final_selector != original_selector:
                        print("💾 Learning new selector...")
                        self.rag_memory.add(
                            text=f"{self.current_step['action']} selector fix",
                            metadata={
                                "type": "selector",
                                "application": "zodiac",
                                "page": self.browser.page.url,
                                "action": self.current_step["action"],
                                "selector": final_selector
                            }
                        )

                else:

                    self.observation = "Action failed"
                    self.retry_count += 1
                    # ✅ ADD HISTORY HERE
                    self.history.append({
                        "step": self.current_step["action"],
                        "action": copy.deepcopy(self.last_decision),
                        "result": self.observation
                    })

                    if len(self.history) > 5:
                        self.history = self.history[-5:]

                    print(f"❌ ACTION FAILED (retry {self.retry_count})")

                    # ✅ RETRY LOGIC (FIRST FIX)
                    if self.retry_count < 2:
                        print("🔁 Retrying step before failure analysis...")

                        # 🔥 ADD THIS
                        self.observation = "Previous action failed. Use selector strictly from visible UI elements."

                        self.state = ReactState.THOUGHT
                        continue

                    # 🔥 ONLY AFTER RETRIES → FAILURE COLLECTION
                    print("❌ RETRIES EXCEEDED — collecting failure evidence")

                    dom = self.browser.extract_dom()
                    optimized_dom = PromptBuilder.build_semantic_dom(dom)

                    collector = FailureCollector(self.browser.page)

                    screenshot_path, json_path = collector.collect(
                        plan=self.plan,
                        current_step=self.current_step,
                        dom=optimized_dom
                    )

                    print("\nSending screenshot to Vision Agent for analysis...\n")

                    analysis = analyze_ui(screenshot_path, self.plan, self.current_step)

                    print("\n🔎 UI ANALYSIS RESULT\n")
                    print(json.dumps(analysis, indent=2))

                    if isinstance(analysis, dict) and analysis.get("error_detected"):
                        print("\n🚨 APPLICATION ERROR DETECTED — stopping test\n")
                        self.state = ReactState.DONE

                        return

                self.state = ReactState.OBSERVE

            ################################################

            elif self.state == ReactState.OBSERVE:

                print("👁 OBSERVATION:", self.observation)

                self.state = ReactState.EVALUATE

            ################################################
            elif self.state == ReactState.EVALUATE:

                if "successfully" in self.observation:

                    print("STEP COMPLETED")
                    self.state = ReactState.DONE

                else:

                    # ❌ REMOVE blind retry
                    # print("Retrying step")
                    # self.state = ReactState.THOUGHT

                    # ✅ Only retry happens in EXECUTE block
                    self.state = ReactState.DONE

            ################################################

            loop_guard += 1