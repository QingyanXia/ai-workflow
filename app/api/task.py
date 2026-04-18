from fastapi import APIRouter
from app.services.task_service import run_task
from app.models.task import Task
from app.storage.task_store import get_task

router = APIRouter()

@router.post("/task")
def create_task(data: dict):
    task = Task(input=data.get("input", ""))
    result = run_task(task)
    return result

@router.get("/task/{task_id}")
def read_task(task_id: str):
    task = get_task(task_id)
    if task is None:
        return {"error": "Task not found"}
    return task