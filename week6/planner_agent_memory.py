import requests


# ------------------------------
# MEMORY
# ------------------------------
memory = {}


# ------------------------------
# LLM
# ------------------------------
def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json().get("response", "")


# ------------------------------
# TOOLS
# ------------------------------
def generate_testcases(feature):

    testcases = f"""
Testcases for {feature}

TC1 Valid login
TC2 Invalid password
TC3 Empty fields
"""

    memory["testcases"] = testcases

    return testcases


def generate_automation(feature):

    testcases = memory.get("testcases", "")

    code = f"""
Playwright automation for {feature}

# Using testcases:
{testcases}

page.goto("/login")
page.fill("#username","user")
page.fill("#password","pass")
page.click("#login")
"""

    memory["automation"] = code

    return code


def validate_code():

    code = memory.get("automation", "")

    if code:
        result = "Code validation successful"
    else:
        result = "No code generated"

    memory["validation"] = result

    return result


# ------------------------------
# PLANNER
# ------------------------------
def create_plan(user_request):
    prompt = f"""
    You are an AI planner.

    Break the user request into exactly three steps.

    Allowed step types:
    Generate testcases
    Generate automation
    Validate code

    Return ONLY these lines:

    Step1 Generate testcases
    Step2 Generate automation
    Step3 Validate code

    Important rules:
    - Do NOT give explanations
    - Do NOT give examples
    - Do NOT repeat steps
    - Return exactly 3 lines

    User request:
    {user_request}
    """

    return ask_llm(prompt)


# ------------------------------
# EXECUTOR
# ------------------------------
def execute_plan(plan, user_request):
    steps = []

    for line in plan.split("\n"):
        line = line.strip()
        if line.lower().startswith("step"):
            steps.append(line)

    steps = steps[:3]

    print("\nExecution started\n")

    result = ""

    for step in steps:

        step = step.lower()

        if "testcase" in step:

            print("Running Step: Generate Testcases\n")
            result = generate_testcases(user_request)
            print(result)

        elif "automation" in step:

            print("Running Step: Generate Automation\n")
            result = generate_automation(user_request)
            print(result)

        elif "validate" in step:

            print("Running Step: Validate Code\n")
            result = validate_code()
            print(result)

    return result


# ------------------------------
# AGENT LOOP
# ------------------------------
def run_agent():

    print("\nPlanner Agent with Memory Started")
    print("Type 'exit' to stop\n")

    while True:

        user_request = input("User: ")

        if user_request == "exit":
            break

        memory.clear()

        print("\nCreating plan...\n")

        plan = create_plan(user_request)

        print("Generated Plan:\n")
        print(plan)

        final_result = execute_plan(plan, user_request)

        print("\nFinal Result:\n")
        print(final_result)
        print()


# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":

    run_agent()