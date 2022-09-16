from typing import Optional
from xml.dom import registerDOMImplementation
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try: 
    conn = psycopg2.connect(host='localhost', port=3306, database='postgres', user='postgres', password='trucktor3', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Connecting from database failed")
    print("Error: ", error)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1}, {
"title": "favorite foods", "content": "I like pizza" , "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        

@app.get("/")
async def root():
    return {"message": "Python API"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    #print(post.dict())
    return {"data": post_dict}
# title str, content str, category, Bool published


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)



