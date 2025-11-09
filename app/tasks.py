from fastapi import APIRouter, Depends
from services.auth import get_current_user
from models.users import User
from services.task_service import Task, TaskCreate, TaskUpdate

app = APIRouter()

# @app.post("/new-task", response_model=dict)
# async def add_new_task(current_user: User = Depends(get_current_user)):
#     """
#     test endpoint that requires auth
#     """
tasks = []


@app.get("/tasks/me", response_model=dict)
async def read_tasks_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "message": "You are authenticated!"}


@app.get("/")
def read_root():
    return {"Hello": "world!"}


@app.post("/tasks/{task_id}")
def create_task(task: str):
    tasks.append(task)
    return tasks


@app.get("/tasks/{task_id, task_desc}")
def get_task(task_id: int, task_desc: str):
    return task_id, task_desc


@app.put("/tasks/{task_id, task_desc}")
def update_task_desc(task_id: int, task_desc: str):
    return {"task_desc": task_desc, "task_id": task_id}
