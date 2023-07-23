from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


@app.get("/")
async def get():
    return {"message": "Hello world"}




@app.get("/blog")
def blogs(limit):
    return{"data": f" {limit}"}

@app.get("/blog/{id}")
def blog(id: int):
    return {"data": {"detail": id}}


class Blog(BaseModel):
    title : str
    body : str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):
    return {"data": f"Blog created with {request.title}"}