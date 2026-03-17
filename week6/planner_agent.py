import requests


# --------------------------------
# LLM FUNCTION
# --------------------------------
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


# --------------------------------
# TOOLS
# --------------------------------
def generate_testcases(feature):

    return f"""
Testcases for {feature}

TC1 Valid scenario
TC2 Invalid scenario
TC3 Edge case
"""


def generate_automation(feature):

    return f"""
Playwright automation example for {feature}

page.goto("/login")
page.fill("#username","user")
page.fill("#password","pass")
page.click("#login")
"""


def validate_code(code):

    return "Code validation successful"


# --------------------------------
# PLANNER
# --------------------------------
def create_plan(user_request):
    prompt = f"""
    You are an AI task planner.

    Break the user request into simple steps.

    Only use the following step types:

    Generate testcases
    Generate automation
    Validate code

    Return steps exactly like this format:

    Step1 Generate testcases
    Step2 Generate automation
    Step3 Validate code

    User request:
    {user_request}
    """

    plan = ask_llm(prompt)

    return plan


# --------------------------------
# EXECUTOR
# --------------------------------
def execute_plan(plan, user_request):

    print("\nExecution started\n")

    result = ""

    steps = plan.split("\n")

    for step in steps:

        step = step.lower()

        if "testcase" in step:

            print("Running Step: Generate Testcases\n")
            result = generate_testcases(user_request)
            print(result)

        elif "automation" in step or "code" in step:

            print("Running Step: Generate Automation\n")
            result = generate_automation(user_request)
            print(result)

        elif "validate" in step:

            print("Running Step: Validate Code\n")
            result = validate_code(result)
            print(result)

    return result


# --------------------------------
# AGENT LOOP
# --------------------------------
def run_agent():

    print("\nPlanner Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        user_request = input("User: ")

        if user_request == "exit":
            break

        print("\nCreating plan...\n")

        plan = create_plan(user_request)

        print("Generated Plan:\n")
        print(plan)

        final_result = execute_plan(plan, user_request)

        print("\nFinal Result:\n")
        print(final_result)
        print()


# --------------------------------
# MAIN
# --------------------------------
if __name__ == "__main__":

    run_agent()