from app.core.llm import call_llm
from app.models.task import Task
from app.storage.task_store import save_task

def run_task(task: Task) -> Task:
    # 任务刚创建，先保存（pending）
    save_task(task)

    task.status = "running"
    save_task(task)

    result = call_llm(task.input)

    task.output = result
    task.status = "finished"
    save_task(task)

    return task