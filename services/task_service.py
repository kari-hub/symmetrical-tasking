from models import Task
from sqlalchemy.orm import Session
from schemas.tasks import TaskCreate, TaskUpdate
from fastapi import HTTPException, status

"""
define the functions to create, get, update and delete tasks
"""


def create_task(db: Session, data: TaskCreate, current_user_id: int):
    new_task = Task(**data.model_dump(), owner_id=current_user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, current_user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    if current_user_id is not None and Task.owner_id is not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your tasks",
        )

    db.delete(task)
    db.commit()
    return {f"Task {Task.title} deleted successfully"}
