from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[
        int, Path(description="The ID of the item to get", gt=0, le=1000)
    ],
):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: str, name: str | None = None):
    if name:
        return {"movie_id": movie_id, "name": name}
    return {"movie_id": movie_id}


@app.get("/test_annotated/")
async def test_annotated(
    q: Annotated[
        str | None,
        Query(
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            alias="item-query",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_name": "Test Annotated"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, description: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if description:
        short = True  # Ensure short is False if description is present
        item.update({"q": description})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item: Item, item_id: int):
    return {"item_id": item_id, **item.model_dump()}


@app.get("/multiple_items/")
async def read_items(q: Annotated[list | None, Query()] = []):
    query_items = {"q": q}
    return query_items
