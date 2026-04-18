from app.core.llm import call_llm
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

    result = call_llm(task.input)

    task.output = result
    task.status = "finished"
    save_task(task)

    return task