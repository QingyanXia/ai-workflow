from app.models.task import Task

task_store: dict[str, Task] = {}

def save_task(task: Task) -> None:
    task_store[task.id] = task

def get_task(task_id: str) -> Task | None:
    return task_store.get(task_id)