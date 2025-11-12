from fastapi import APIRouter, Depends, status, HTTPException
from services.auth import get_current_user
from models.users import User
from sqlalchemy.orm import Session
from db import get_db
from typing import List
from schemas.tasks import TaskCreate, TaskUpdate, Task
from services.task_service import (
    get_task,
    get_all_tasks,
    create_task,
    update_task,
    delete_task,
)

router = APIRouter(tags=["Tasks APIs"])

# @app.post("/new-task", response_model=dict)
# async def add_new_task(current_user: User = Depends(get_current_user)):
#     """
#     test endpoint that requires auth
#     """
tasks = []


@router.post(
    "/tasks",
    response_model=Task,
    summary="Create a new task and assign to a user",
    status_code=status.HTTP_201_CREATED,
)
def create_new_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, task_in, current_user.id)


@router.get("/tasks/{task_id}", response_model=Task, summary="Get a single task")
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.get("/tasks", response_model=List[Task], summary="Get all current tasks")
def read_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)


@router.patch("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task_desc(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = update_task(db, task_id, task_in)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_task(db, task_id, current_user.id)
    return None  # 204 content
