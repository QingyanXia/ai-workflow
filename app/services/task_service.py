from app.core.llm import call_llm
from app.core.planner import plan_steps
from app.models.task import Task
from app.storage.task_store import save_task, get_task
from app.core.validator import check_task_feasibility

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

    # 在 planner 之前做判断
    feasibility = check_task_feasibility(task.input)

    if not feasibility["physical_feasible"]:
        task.status = "failed"
        task.output = feasibility["reason"]
        save_task(task)
        return task

    # 不该做的暂时不阻断，只记录
    if not feasibility["should_execute"]:
        task.output = feasibility["reason"]
        save_task(task)
    # ↓↓↓ 只有通过检查才继续

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
    Return only the result.
    """
        result = call_llm(prompt)

        # 判断失败（最小规则）
        if not result or len(result.strip()) < 3:
            step.output = result
            step.status = "failed"

            task.status = "failed"
            save_task(task)

            return task  # 直接终止整个任务

        step.output = result
        step.status = "finished"
        save_task(task)

        context += f"Step {i + 1}: {step.description}\nResult: {step.output}\n\n"

    # 3. 汇总结果
    task.output = "\n\n".join(
        f"Step {i+1}: {step.description}\n{step.output}"
        for i, step in enumerate(task.steps)
    )
    task.status = "finished"
    save_task(task)

    return task