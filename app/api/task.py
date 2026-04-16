from fastapi import APIRouter
from app.services.task_service import run_task
from app.models.task import Task

router = APIRouter()

@router.post("/task")
def create_task(data: dict):
    task = Task(input=data.get("input", ""))
    result = run_task(task)
    return result