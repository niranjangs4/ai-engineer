import requests

# -----------------------------
# MEMORY
# -----------------------------

memory = {}

# -----------------------------
# LLM
# -----------------------------

def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# -----------------------------
# AUTOMATION TOOLS
# -----------------------------

def generate_testcases(feature):

    testcases = f"""
Testcases for {feature}

TC1 Valid login
TC2 Invalid password
TC3 Empty fields
"""

    memory["testcases"] = testcases
    return testcases


def generate_playwright_code(feature):

    code = f"""
Playwright Test Script for {feature}

test('login test', async ({{ page }}) => {{

  await page.goto("/login")

  await page.fill("#username", "user")

  await page.fill("#password", "pass")

  await page.click("#login")

}})
"""

    memory["automation_code"] = code
    return code


def run_playwright_tests():

    results = {
        "total": 3,
        "passed": 2,
        "failed": 1
    }

    memory["test_results"] = results

    return f"""
Test Execution Results

Total: {results["total"]}
Passed: {results["passed"]}
Failed: {results["failed"]}
"""


def analyze_failures():

    analysis = "Login button locator may have changed"

    memory["failure_analysis"] = analysis

    return analysis


def generate_report():

    report = f"""
Automation Report

Testcases:
{memory.get("testcases")}

Automation Code:
{memory.get("automation_code")}

Test Results:
{memory.get("test_results")}

Failure Analysis:
{memory.get("failure_analysis")}
"""

    memory["report"] = report

    return report


# -----------------------------
# TOOL REGISTRY
# -----------------------------

tools = {
    "generate_testcases": generate_testcases,
    "generate_playwright_code": generate_playwright_code,
    "run_playwright_tests": run_playwright_tests,
    "analyze_failures": analyze_failures,
    "generate_report": generate_report
}


# -----------------------------
# PLANNER
# -----------------------------

def create_plan(user_request):

    prompt = f"""
You are a QA automation planner.

Break the task into steps.

Return ONLY these steps:

Step1 Generate testcases
Step2 Generate automation
Step3 Run tests
Step4 Analyze failures
Step5 Generate report

User request:
{user_request}
"""

    return ask_llm(prompt)


# -----------------------------
# EXECUTOR
# -----------------------------

def execute_step(step, user_request):

    step = step.lower()

    if "testcase" in step:
        return tools["generate_testcases"](user_request)

    if "automation" in step:
        return tools["generate_playwright_code"](user_request)

    if "run tests" in step:
        return tools["run_playwright_tests"]()

    if "analyze" in step:
        return tools["analyze_failures"]()

    if "report" in step:
        return tools["generate_report"]()


# -----------------------------
# REFLECTION
# -----------------------------

def reflect(result):

    prompt = f"""
Review the following result.

If it is correct respond with:
SUCCESS

If there is a problem respond with:
ISSUE: <short reason>

Result:
{result}
"""

    return ask_llm(prompt)


# -----------------------------
# AGENT CONTROLLER
# -----------------------------

def run_agent():

    print("\nAutomation Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        user_request = input("User: ")

        if user_request == "exit":
            break

        memory.clear()

        print("\nCreating automation plan...\n")

        plan = create_plan(user_request)

        print("Plan:\n")
        print(plan)

        steps = [s for s in plan.split("\n") if s.lower().startswith("step")]

        for step in steps:

            print(f"\nExecuting: {step}")

            result = execute_step(step, user_request)

            print("\nResult:\n", result)

            reflection = reflect(result)

            print("\nReflection:", reflection)

        print("\nFinal Automation Report:\n")

        print(memory.get("report"))


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    run_agent()