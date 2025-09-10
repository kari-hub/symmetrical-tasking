# from typing import Union
from fastapi import FastAPI
import uvicorn
# from pydantic import BaseModel
# from fastapi import Depends

app = FastAPI()

tasks = []


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


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item_name, "item_id": item_id}
