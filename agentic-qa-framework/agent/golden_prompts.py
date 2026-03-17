import json
from framework.load_tools import load_tools

def build_tool_list():
    return load_tools()
def safe_text(text):
    if not text:
        return ""
    return text.replace("{", "").replace("}", "").replace("```", "")
class PromptBuilder:

    @staticmethod
    def react(goal, plan_step, dom, observation, rag_memory, history, tools):
        # build readable tool list
        tool_list = "\n".join(tools.keys())
        filtered_memory = []

        memory_list = rag_memory if isinstance(rag_memory, list) else rag_memory.data

        for item in memory_list:
            meta = item.get("metadata", {})
            if meta.get("type") in ["selector", "workflow"]:
                filtered_memory.append(meta)
        prompt = f"""
    You are an AI web automation executor using the ReAct method.

    Your job is to execute ONLY the CURRENT PLAN STEP.

    ----------------------------------------
    GOAL
    ----------------------------------------
    {goal}

    ----------------------------------------
    CURRENT PLAN STEP
    ----------------------------------------
    {plan_step}

    ----------------------------------------
    VISIBLE UI ELEMENTS
    ----------------------------------------
    {json.dumps(dom, indent=2)}

    ----------------------------------------
    APPLICATION KNOWLEDGE (RAG MEMORY)
    ----------------------------------------
    {json.dumps(filtered_memory[:5], indent=2)}

    ----------------------------------------
    PREVIOUS ACTION HISTORY
    ----------------------------------------
    {history}

    ----------------------------------------
    OBSERVATION FROM LAST ACTION
    ----------------------------------------
    {observation}

    ----------------------------------------
    AVAILABLE TOOLS
    ----------------------------------------
    {tool_list}

    Valid actions are the tool names above or "done".

    ----------------------------------------
    IMPORTANT SELECTOR RULE
    ----------------------------------------

    Selectors in VISIBLE UI ELEMENTS are already valid.

    Example element:

    {{
    "type": "button",
    "text": "Sign In",
    "selector": "button:has-text('Sign In')"
    }}

    You MUST use selectors exactly as provided.

    Do NOT generate new selectors unless absolutely necessary.
    Prefer selectors from UI or memory.
    Do NOT modify selectors.
    Do NOT invent selectors.

    ----------------------------------------
    SELECTOR PRIORITY
    ----------------------------------------

    1. If APPLICATION KNOWLEDGE (RAG MEMORY) contains a selector, use it first.

    2. Otherwise find the matching element from VISIBLE UI ELEMENTS
       and use the selector provided there.

    3. Never invent new selectors.

    ----------------------------------------
    EXECUTION RULES
    ----------------------------------------

    1. Think step-by-step.
    2. Focus ONLY on the CURRENT PLAN STEP.
    3. Do NOT jump ahead to future steps.
    4. If the step is already completed based on OBSERVATION, return action_type="done".
    5. Do NOT repeat actions that already succeeded.

    ----------------------------------------
    OUTPUT FORMAT
    ----------------------------------------

    Return JSON only.

    {{
    "thought": "",
    "action_type": "",
    "target_text": "",
    "target_url": "",
    "selector": "",
    "value": ""
    }}
    """

        return prompt




    @staticmethod
    def build_semantic_dom(dom):

        elements = []

        for el in dom:

            tag = el.get("tag")
            text = safe_text((el.get("text") or "").strip())
            el_id = el.get("id")
            name = el.get("name")
            placeholder = el.get("placeholder")
            el_type = el.get("type")

            selector = None

            if el_id:
                selector = f"#{el_id}"

            elif name:
                selector = f'{tag}[name="{name}"]'

            elif placeholder:
                selector = f'{tag}[placeholder="{placeholder}"]'

            elif tag == "button" and text:
                selector = f'button:has-text("{text}")'

            elif tag == "a" and text:
                selector = f'a:has-text("{text}")'

            if selector:
                elements.append({
                    "type": tag,
                    "text": text,
                    "selector": selector
                })

        return elements
    ############################################################
    # PLANNER PROMPT
    ############################################################

    @staticmethod
    def planner(goal, rag_memory):
        filtered_memory = []

        memory_list = rag_memory if isinstance(rag_memory, list) else rag_memory.data

        for item in memory_list:
            meta = item.get("metadata", {})
            if meta.get("type") in ["selector", "workflow"]:
                filtered_memory.append(meta)
        prompt = f"""
        You are a QA automation planner.
        
        Your job is to create a step-by-step execution plan for a web automation agent.
        
        GOAL
        {goal}
        
        APPLICATION KNOWLEDGE (RAG MEMORY)
        {json.dumps(filtered_memory[:5], indent=2)}
        
        RULES
        
        1. Use APPLICATION KNOWLEDGE when relevant.
        2. Each step must represent ONE UI interaction.
        3. Steps must follow logical workflow order.
        4. Do NOT generate unnecessary steps.
        5. Keep the plan minimal.
        6. Each step action must map to an AVAILABLE TOOL (e.g., click, fill_input, open_url).
        7. Do NOT create abstract steps like "login user".
        
        Return JSON only.
        
        {{
         "plan":[
          {{
           "step":1,
           "action":"",
           "expected_result":"",
           "done":false
          }}
         ]
        }}
        """

        # print("\n========== PLANNER PROMPT ==========\n")
        # print(prompt)
        # print("\n====================================\n")

        return prompt

    ############################################################
    # REACT EXECUTION PROMPT
    ############################################################



    @staticmethod
    def build_prompt(method_name, framework, language):
        prompt = f"""
    You are a senior automation engineer.

    Create a reusable automation function.

    Method Name:
    {method_name}

    Framework:
    {framework}

    Language:
    {language}

    Requirements:
    - Use Playwright
    - Add error handling
    - Wait for page load
    - Return useful output
    - Production quality code

    Return ONLY the function code.
    """

        return prompt