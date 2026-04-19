from app.core.llm import call_llm
from app.models.task import Task
from app.storage.task_store import save_task, get_task
from app.core.planner import plan_steps

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

    # 新增：先拆任务
    steps = plan_steps(task.input)
    task.steps = steps
    save_task(task)

    # （暂时不执行步骤）
    task.status = "finished"
    save_task(task)

    return task