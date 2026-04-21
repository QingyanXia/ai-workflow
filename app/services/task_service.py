from app.core.llm import call_llm
from app.core.planner import plan_steps
from app.models.task import Task
from app.storage.task_store import save_task, get_task

def create_task(user_input: str) -> Task:
    task = Task(input=user_input)
    save_task(task)
    return task

def run_task(task_id: str) -> Task | None:
    task = get_task(task_id)
    if task is None:
        return None

    if task.status != "pending":
        return task

    task.status = "running"
    save_task(task)

    # 1. 生成步骤
    task.steps = plan_steps(task.input)
    save_task(task)

    # 2. 顺序执行，并传递上下文
    context = ""

    for i, step in enumerate(task.steps):
        step.status = "running"

        step.input = f"""Original task:
{task.input}

Previous completed steps:
{context if context else "None"}

Current step:
{step.description}
"""
        save_task(task)

        prompt = f"""
You are executing one step in a larger task.

Original task:
{task.input}

Previous completed steps:
{context if context else "None"}

Current step:
{step.description}

Please complete only the current step.
Use the previous completed steps as context when necessary.
Return only the result of this step.
"""
        result = call_llm(prompt)

        step.output = result
        step.status = "finished"
        save_task(task)

        context += f"Step {i+1}: {step.description}\nResult: {step.output}\n\n"

    # 3. 汇总结果
    task.output = "\n\n".join(
        f"Step {i+1}: {step.description}\n{step.output}"
        for i, step in enumerate(task.steps)
    )
    task.status = "finished"
    save_task(task)

    return task