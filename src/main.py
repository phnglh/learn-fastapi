# from typing import Union

from fastapi import FastAPI, Query, APIRouter, Body
from typing import Annotated, Set
from pydantic import BaseModel, Field
app = FastAPI()

api_router = APIRouter(prefix="/api")


fake_items_db=[{"item_name": "phong"},{"item_name": "huy"},{"item_name": "huyen"}]

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300, examples=["A very nice Item"]
    )
    price: float
    tax: float | None = None
    tags: Set[str] = set()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": ["iphone", "mobile"]
                }
            ]
        }
    }

@api_router.get("/")
def read_root():
    return {"Hello": "World"}

@api_router.get("/items")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items

@api_router.get("/items/{item_id}")
def read_item(item_id: int, q: Annotated[str| None, Query(min_length=3, max_length=30)] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@api_router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results 

@app.post("/no_embed")
def no_embed(item: Item):
    return item

@app.post("/with_embed")
def with_embed(item: Annotated[Item, Body(embed=True)]):
    return item


app.include_router(api_router)
