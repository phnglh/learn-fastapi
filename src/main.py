from typing import Union

from fastapi import FastAPI, Query
from typing import Annotated
app = FastAPI() 


fake_items_db=[{"item_name": "phong"},{"item_name": "huy"},{"item_name": "huyen"}]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Annotated[str| None, Query(min_length=3, max_length=30)] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
