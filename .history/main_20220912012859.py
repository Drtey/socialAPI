from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = none


@app.get("/")
async def root():
    return {"message": "Python API"}

@app.post("/cpost")
def cpost(post: Post):
    print(post.published)
    return {"data": "new post"}
# title str, content str, category, Bool published