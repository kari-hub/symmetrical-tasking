from fastapi import FastAPI
from app.auth import app as auth_router
from app.tasks import app as task_router
# from fastapi import Depends

app = FastAPI()

# include routers
app.include_router(auth_router)
app.include_router(task_router)

# tasks = []


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item_name, "item_id": item_id}
