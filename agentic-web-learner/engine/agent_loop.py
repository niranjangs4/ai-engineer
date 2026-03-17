# from __future__ import annotations
#
# from dataclasses import asdict
#
# from agents.planner_agent import PlannerAgent
# from agents.react_agent import ReactAgent
# from crawler.crawler_engine import CrawlerEngine
# from engine.failure_detector import FailureDetector
# from engine.llm_reasoning_engine import LLMReasoningEngine
# from memory.navigation_graph import NavigationGraph
# from rag.retrieval_engine import RetrievalEngine
# from testing.test_generator import TestGenerator
# from utils.logger import configure_logging, log_block
#
#
# class AgentLoop:
#     def __init__(
#         self,
#         crawler_engine: CrawlerEngine,
#         planner_agent: PlannerAgent,
#         react_agent: ReactAgent,
#         reasoning_engine: LLMReasoningEngine,
#         failure_detector: FailureDetector,
#         retrieval_engine: RetrievalEngine,
#         navigation_graph: NavigationGraph,
#         test_generator: TestGenerator,
#         log_level: str = "INFO",
#     ) -> None:
#         self.crawler_engine = crawler_engine
#         self.planner_agent = planner_agent
#         self.react_agent = react_agent
#         self.reasoning_engine = reasoning_engine
#         self.failure_detector = failure_detector
#         self.retrieval_engine = retrieval_engine
#         self.navigation_graph = navigation_graph
#         self.test_generator = test_generator
#         self.logger = configure_logging(log_level)
#
#     def run(self, goal: str, max_steps: int) -> dict:
#         plan = self.planner_agent.create_plan(goal)
#         log_block(self.logger, "Execution Plan", "\n".join(plan) or "No plan returned.")
#
#         discovered_pages: list[str] = []
#         previous_summary: dict | None = None
#         previous_state = None
#         action_history: list[str] = []
#         stop_reason = "max_steps_reached"
#
#         for step_index in range(max_steps):
#             step_number = step_index + 1
#             current_state, _, page_summary = self.crawler_engine.observe_page()
#             log_block(self.logger, "Capture DOM", str(page_summary), step=step_number)
#             if current_state.url not in discovered_pages:
#                 discovered_pages.append(current_state.url)
#
#             rag_context = self._retrieve_context(page_summary)
#             log_block(self.logger, "RAG Context", str(rag_context), step=step_number)
#             react_step = self.react_agent.decide_next_action(
#                 goal=goal,
#                 page_summary=page_summary,
#                 visited_actions=action_history,
#                 rag_context=rag_context,
#                 source_page=current_state.url,
#             )
#             if react_step.action is None:
#                 stop_reason = "no_action_returned"
#                 self.logger.info("Ollama did not return another action. Agent loop complete.")
#                 break
#
#             log_block(self.logger, "Agent Thought", str(react_step.thought), step=step_number)
#             log_block(
#                 self.logger,
#                 "Selected Action",
#                 f"type={react_step.action.action_type}\ntarget={react_step.action.target_text or react_step.action.text}\nvalue={react_step.action.value}",
#                 step=step_number,
#             )
#             log_block(self.logger, "Action Payload", str(asdict(react_step.action)), step=step_number)
#             action_history.append(f"{react_step.action.action_type}:{react_step.action.text}")
#
#             executed = self._execute_with_recovery(
#                 step_index=step_number,
#                 goal=goal,
#                 initial_action=react_step.action,
#                 current_url=current_state.url,
#                 action_history=action_history,
#             )
#             if not executed:
#                 stop_reason = "action_failed_after_retries"
#                 self.crawler_engine.state_manager.mark_action_failed(react_step.action)
#                 report = self.failure_detector.create_report(
#                     summary="Browser action failed after retries",
#                     actual_result=f"Action {react_step.action.action_type} on {react_step.action.text} could not be executed.",
#                     url=current_state.url,
#                     prompt_trace=self.reasoning_engine.combined_trace(),
#                     steps_to_reproduce=self._steps_for_bug(current_state.url, react_step.action),
#                 )
#                 self.crawler_engine.state_manager.record_failure(report)
#                 break
#
#             self.crawler_engine.state_manager.mark_action_visited(react_step.action)
#
#             # Always capture a fresh DOM after every action.
#             new_state, _, new_summary = self.crawler_engine.observe_page()
#             log_block(self.logger, "Fresh DOM After Action", str(new_summary), step=step_number)
#             state_context = self._retrieve_context(new_summary)
#             transition = self.reasoning_engine.assess_transition(
#                 goal=goal,
#                 previous_summary=previous_summary or page_summary,
#                 current_summary=new_summary,
#                 rag_context=state_context,
#                 action_history=action_history,
#             )
#             log_block(self.logger, "Page State Change", str(transition), step=step_number)
#
#             self.crawler_engine.memory_agent.remember_records(transition.get("memory_records", []))
#
#             if previous_state and transition.get("changed"):
#                 self.navigation_graph.add_edge(previous_state.url, new_state.url, action_label=react_step.action.text)
#
#             if transition.get("failed"):
#                 stop_reason = "transition_failed"
#                 report = self.failure_detector.create_report(
#                     summary=transition.get("summary", "Agentic browser step failed"),
#                     actual_result=transition.get("actual_result", "The LLM flagged the step as failed."),
#                     url=new_state.url,
#                     prompt_trace=self.reasoning_engine.combined_trace(),
#                     steps_to_reproduce=self._steps_for_bug(current_state.url, react_step.action),
#                 )
#                 self.crawler_engine.state_manager.record_failure(report)
#                 break
#
#             if self._navigation_detected(current_state.url, new_state.url):
#                 stop_reason = "page_navigation_detected"
#                 self.logger.info("Navigation detected from %s to %s. Agent loop complete.", current_state.url, new_state.url)
#                 previous_summary = new_summary
#                 previous_state = new_state
#                 break
#
#             if self._goal_achieved(goal, new_summary):
#                 stop_reason = "goal_achieved"
#                 self.logger.info("Goal achieved based on the latest DOM state. Agent loop complete.")
#                 previous_summary = new_summary
#                 previous_state = new_state
#                 break
#
#             previous_summary = new_summary
#             previous_state = new_state
#
#             if step_index == max_steps - 1:
#                 self.logger.info("Reached maximum configured steps.")
#
#         generated_tests = self.test_generator.generate()
#         return {
#             "plan": plan,
#             "discovered_pages": discovered_pages,
#             "generated_tests": generated_tests,
#             "failure_reports": self.crawler_engine.state_manager.failure_reports,
#             "stop_reason": stop_reason,
#         }
#
#     def _retrieve_context(self, page_summary: dict) -> dict:
#         query = " ".join(
#             [
#                 page_summary.get("title", ""),
#                 page_summary.get("url", ""),
#                 " ".join(element.get("text", "") for element in page_summary.get("elements", [])[:10]),
#             ]
#         ).strip()
#         if not query:
#             return {}
#         raw = self.retrieval_engine.retrieve(query, limit=2)
#         documents = raw.get("documents", [[]])
#         metadatas = raw.get("metadatas", [[]])
#         compact_items: list[dict] = []
#         for document, metadata in zip(documents[0] if documents else [], metadatas[0] if metadatas else []):
#             compact_items.append(
#                 {
#                     "text": (metadata.get("text") if isinstance(metadata, dict) else "") or str(document)[:80],
#                     "type": metadata.get("type") if isinstance(metadata, dict) else "",
#                     "container": metadata.get("container") if isinstance(metadata, dict) else "",
#                 }
#             )
#         return {"items": compact_items}
#
#     def _execute_with_recovery(self, step_index: int, goal: str, initial_action, current_url: str, action_history: list[str]) -> bool:
#         action = initial_action
#         for attempt in range(1, 4):
#             log_block(
#                 self.logger,
#                 "Tool Execution",
#                 f'{action.action_type}("{action.target_text or action.text}")',
#                 step=step_index,
#             )
#             if self.crawler_engine.browser.execute_action(action):
#                 log_block(self.logger, "Tool Result", "Action executed successfully.", step=step_index)
#                 return True
#
#             log_block(
#                 self.logger,
#                 "Error",
#                 f"Action failed.\nRetry attempt: {attempt}\nCurrent URL: {current_url}",
#                 step=step_index,
#             )
#             fresh_state, _, fresh_summary = self.crawler_engine.observe_page()
#             log_block(self.logger, "Recovery DOM", str(fresh_summary), step=step_index)
#             rag_context = self._retrieve_context(fresh_summary)
#             log_block(self.logger, "Recovery RAG Context", str(rag_context), step=step_index)
#             recovery_decision = self.reasoning_engine.decide_recovery_action(
#                 goal=goal,
#                 failed_action=f"{action.action_type}:{action.target_text or action.text}",
#                 error_message="The previous browser tool could not find or complete the intended interaction.",
#                 page_summary=fresh_summary,
#                 rag_context=rag_context,
#                 action_history=action_history,
#             )
#             log_block(self.logger, "Recovery Decision", str(recovery_decision), step=step_index)
#             self.crawler_engine.memory_agent.remember_records(recovery_decision.get("memory_records", []))
#             recovery_action = self.reasoning_engine.build_action(
#                 recovery_decision,
#                 source_page=fresh_state.url,
#             )
#             if recovery_action is None:
#                 return False
#             log_block(
#                 self.logger,
#                 "Recovery Triggered",
#                 f"blocking_element={recovery_decision.get('blocking_element', '')}\n"
#                 f"new_action={recovery_action.action_type}:{recovery_action.target_text or recovery_action.text}",
#                 step=step_index,
#             )
#             log_block(self.logger, "Recovery Action Payload", str(asdict(recovery_action)), step=step_index)
#             action_history.append(f"recovery:{recovery_action.action_type}:{recovery_action.text}")
#             action = recovery_action
#         return False
#
#     def _steps_for_bug(self, url: str, action) -> list[str]:
#         return [
#             f"Navigate to {url}",
#             "Allow the agent to capture a fresh DOM snapshot",
#             f"Let Ollama choose the next action: {action.action_type} -> {action.text}",
#             "Observe the resulting page behavior and failure condition",
#         ]
#
#     def _navigation_detected(self, previous_url: str, current_url: str) -> bool:
#         return bool(previous_url and current_url and previous_url != current_url)
#
#     def _goal_achieved(self, goal: str, page_summary: dict) -> bool:
#         goal_text = goal.lower()
#         elements = page_summary.get("elements", [])
#         element_text = " ".join(str(element.get("text", "")).lower() for element in elements)
#         if "log into" in goal_text or "login" in goal_text:
#             login_markers = ("user-id", "username", "email", "password", "sign in", "login")
#             return not any(marker in element_text for marker in login_markers)
#         return False
