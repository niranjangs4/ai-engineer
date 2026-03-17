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
# TOOLS
# -----------------------------

def generate_testcases(feature):

    testcases = f"""
Testcases for {feature}

TC1 Valid scenario
TC2 Invalid scenario
TC3 Edge case
"""

    memory["testcases"] = testcases
    return testcases


def generate_automation(feature):

    testcases = memory.get("testcases", "")

    code = f"""
Playwright automation for {feature}

# Using testcases
{testcases}

page.goto("/login")
page.fill("#username","user")
page.fill("#password","pass")
page.click("#login")
"""

    memory["automation"] = code
    return code


def run_tests():

    result = "2 tests passed, 1 failed"
    memory["test_results"] = result
    return result


def analyze_failures():

    analysis = "Locator for login button may have changed"
    memory["analysis"] = analysis
    return analysis


def generate_report():

    report = f"""
Automation Report

Testcases:
{memory.get("testcases")}

Automation Code:
{memory.get("automation")}

Test Results:
{memory.get("test_results")}

Failure Analysis:
{memory.get("analysis")}
"""

    return report


# -----------------------------
# TOOL REGISTRY
# -----------------------------

tools = {
    "generate_testcases": generate_testcases,
    "generate_automation": generate_automation,
    "run_tests": run_tests,
    "analyze_failures": analyze_failures,
    "generate_report": generate_report
}


# -----------------------------
# PLANNER
# -----------------------------

def create_plan(user_request):
    prompt = f"""
    You are an AI planner.

    Break the task into exactly these steps.

    Return ONLY these lines:

    Step1 Generate testcases
    Step2 Generate automation
    Step3 Run tests
    Step4 Analyze failures
    Step5 Generate report

    Do not add explanations.
    Do not add extra steps.
    Do not add 'Step end'.

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
        tool = tools["generate_testcases"]
        return tool(user_request)

    if "automation" in step:
        tool = tools["generate_automation"]
        return tool(user_request)

    if "run tests" in step:
        tool = tools["run_tests"]
        return tool()

    if "analyze" in step:
        tool = tools["analyze_failures"]
        return tool()

    if "report" in step:
        tool = tools["generate_report"]
        return tool()


# -----------------------------
# REFLECTION
# -----------------------------

def reflect(result):
    prompt = f"""
    You are reviewing the result of an AI agent step.

    Respond in ONE short sentence.

    If result looks correct say:
    SUCCESS

    If there is a problem say:
    ISSUE: <short reason>

    Result:
    {result}
    """

    return ask_llm(prompt)


# -----------------------------
# AGENT
# -----------------------------

def run_agent():

    print("\nCombined Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        user_request = input("User: ")

        if user_request == "exit":
            break

        memory.clear()

        print("\nCreating plan...\n")

        plan = create_plan(user_request)

        print("Plan:\n")
        print(plan)

        steps = []

        for line in plan.split("\n"):

            line = line.strip()

            if line.startswith("Step1") or \
                    line.startswith("Step2") or \
                    line.startswith("Step3") or \
                    line.startswith("Step4") or \
                    line.startswith("Step5"):
                steps.append(line)

        for step in steps:

            print(f"\nExecuting: {step}\n")

            result = execute_step(step, user_request)

            print("Result:\n", result)

            reflection = reflect(result)

            print("\nReflection:\n", reflection)

        print("\nFinal Report:\n")
        print("\nFinal Report:\n")

        report = generate_report()

        print(report)


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    run_agent()