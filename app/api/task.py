from fastapi import APIRouter
from app.services.task_service import run_task

router = APIRouter()

@router.post("/task")
def create_task(data: dict):
    user_input = data.get("input", "")
    result = run_task(user_input)
    return {"result": result}