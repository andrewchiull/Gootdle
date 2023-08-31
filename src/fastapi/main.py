import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    slot: int
    recommendations: List[int]




app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = list()
confirm = list()

@app.get("/")
async def root():
    return "Hello, Gootdle!"
@app.get("/items")
async def get_items():
    return items

@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return f"{item} has been added in to {items !r}!"

@app.post("/items/confirm")
async def confirm_item(item: Item):
    confirm.append(item)
    return f"{item} confirmed! Added in to {confirm !r}!"