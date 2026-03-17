from __future__ import annotations

from agents.memory_agent import MemoryAgent
from agents.planner_agent import PlannerAgent
from agents.react_agent import ReactAgent
from browser.browser_controller import BrowserController
from browser.dom_observer import DOMObserver
from browser.page_state_detector import PageStateDetector
from config.settings import settings
from crawler.crawler_engine import CrawlerEngine
from engine.agent_loop import AgentLoop
from engine.failure_detector import FailureDetector
from engine.llm_reasoning_engine import LLMReasoningEngine
from engine.prompt_engine import GoldenPromptEngine
from engine.state_manager import StateManager
from memory.fingerprint_store import FingerprintStore
from memory.navigation_graph import NavigationGraph
from memory.vector_store import VectorStore
from rag.embedding_model import EmbeddingModel
from rag.retrieval_engine import RetrievalEngine
from testing.test_generator import TestGenerator
from utils.loggerfw import build_log_file, configure_logging, log_block


def main() -> None:
    log_file = build_log_file(settings.logs_path) if settings.debug_mode else None
    logger = configure_logging(settings.log_level, log_file=log_file)
    log_block(
        logger,
        "Runtime Inputs",
        "\n".join(
            [
                f"log_file={log_file}",
                f"login_url={settings.login_url}",
                f"max_steps={settings.max_steps}",
                f"ollama_model={settings.ollama_model}",
                f"ollama_url={settings.ollama_url}",
                f"headless={settings.headless}",
                f"debug_mode={settings.debug_mode}",
            ]
        ),
    )

    embedding_model = EmbeddingModel(settings)
    vector_store = VectorStore(settings, embedding_model)
    retrieval_engine = RetrievalEngine(vector_store)
    navigation_graph = NavigationGraph()
    fingerprint_store = FingerprintStore()
    memory_agent = MemoryAgent(vector_store, navigation_graph, fingerprint_store)

    prompt_engine = GoldenPromptEngine("prompts")
    reasoning_engine = LLMReasoningEngine(settings, prompt_engine)
    planner_agent = PlannerAgent(reasoning_engine)
    react_agent = ReactAgent(reasoning_engine)

    browser = BrowserController(settings)
    dom_observer = DOMObserver()
    page_state_detector = PageStateDetector()
    state_manager = StateManager(max_depth=settings.max_depth)
    failure_detector = FailureDetector(browser, settings)
    crawler_engine = CrawlerEngine(
        browser=browser,
        dom_observer=dom_observer,
        page_state_detector=page_state_detector,
        memory_agent=memory_agent,
        state_manager=state_manager,
        failure_detector=failure_detector,
    )
    test_generator = TestGenerator(navigation_graph)
    agent_loop = AgentLoop(
        crawler_engine=crawler_engine,
        planner_agent=planner_agent,
        react_agent=react_agent,
        reasoning_engine=reasoning_engine,
        failure_detector=failure_detector,
        retrieval_engine=retrieval_engine,
        navigation_graph=navigation_graph,
        test_generator=test_generator,
        log_level=settings.log_level,
    )

    try:
        browser.open_url(settings.login_url)
        try:
            goal = "Accept All Cookies and Log into the application, understand the UI, and learn the website for future automation."
            log_block(logger, "Agent Goal", goal)
            result = agent_loop.run(
                goal=goal,
                max_steps=settings.max_steps,
            )
        except Exception as exc:
            report = failure_detector.create_report(
                summary="Unhandled agent loop exception",
                actual_result=str(exc),
                url=browser.current_url(),
                prompt_trace=reasoning_engine.combined_trace(),
            )
            result = {
                "plan": [],
                "discovered_pages": [browser.current_url()],
                "generated_tests": [],
                "failure_reports": [report],
            }
        graph_text = navigation_graph.visualize(settings.graph_output)

        print("Discovered pages:")
        for page in result["discovered_pages"]:
            print(f"- {page}")

        if result["failure_reports"]:
            print("\nFailure reports:")
            for report in result["failure_reports"]:
                print(f"- {report.summary}")
                print(report.jira_ticket)

        print("\nNavigation graph:")
        print(graph_text or "(graph is empty)")

        print("\nGenerated tests:")
        for test in result["generated_tests"]:
            print(f"- {test.name}: {' -> '.join(test.steps)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()
