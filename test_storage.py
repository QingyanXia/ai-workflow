from app.models.task import Task
from app.storage.task_store import save_task, get_task

task = Task(input="hello")
save_task(task)

loaded_task = get_task(task.id)

print(task)
print(loaded_task)
print(task.id == loaded_task.id)