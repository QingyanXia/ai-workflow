import re
from app.core.llm import call_llm
from app.models.step import Step

def plan_steps(task_input: str) -> list[Step]:
    prompt = f"""
You are a task planner for an AI workflow system.
Break the following task into 3 to 6 clear, high-level, ordered steps.

Requirements:
- Each step should be short and actionable
- Focus on execution flow, not detailed writing outline
- Return only the steps
- One step per line
- Do not add explanations

Task:
{task_input}
"""
    response = call_llm(prompt)

    steps = []
    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        line = re.sub(r"^-+\s*", "", line)

        if line:
            step = Step(description=line)
            steps.append(step)

    return steps