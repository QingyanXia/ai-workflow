from app.core.llm import call_llm

def check_task_feasibility(task_input: str) -> dict:
    prompt = f"""
You are a task feasibility checker for an AI workflow system.

Your job is NOT to solve the task.
Your job is to classify the task in two dimensions.

Task:
{task_input}

Dimension 1: physical_feasibility
- Whether the task is logically or physically possible under the stated conditions.
- Do not add unstated assumptions, tools, materials, or conditions.

Dimension 2: execution_suitability
- Whether executing the task may involve harm, danger, illegal activity, or unsafe treatment.
- This does NOT determine physical feasibility.

Return only in this exact format:

physical_feasible: yes/no
should_execute: yes/no
reason: short explanation
"""

    response = call_llm(prompt)
    lower = response.lower()

    physical_feasible = "physical_feasible: yes" in lower
    should_execute = "should_execute: yes" in lower

    return {
        "physical_feasible": physical_feasible,
        "should_execute": should_execute,
        "reason": response
    }