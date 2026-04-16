from app.core.llm import call_llm
from app.models.task import Task

def run_task(task: Task) -> Task:
    task.status = "running"

    result = call_llm(task.input)

    task.output = result
    task.status = "finished"

    return task