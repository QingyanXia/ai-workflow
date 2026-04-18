from fastapi import APIRouter
from app.services.task_service import create_task, run_task
from app.storage.task_store import get_task

router = APIRouter()

@router.post("/task")
def create_new_task(data: dict):
    user_input = data.get("input", "")
    task = create_task(user_input)
    return task

@router.post("/task/{task_id}/run")
def run_existing_task(task_id: str):
    task = run_task(task_id)
    if task is None:
        return {"error": "Task not found"}
    return task

@router.get("/task/{task_id}")
def read_task(task_id: str):
    task = get_task(task_id)
    if task is None:
        return {"error": "Task not found"}
    return task