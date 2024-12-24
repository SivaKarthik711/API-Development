from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException #Fastapi documentation under Tutorial-Userguide\First Steps
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI() #instance

class Post(BaseModel): #this class is to check the schema is followed by front end , when it request API server by using pydantic library 
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None #some might give rating or may not, so considering it as optional by default it is set None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return i
        
def find_index_post(id):
    for i, p  in enumerate(my_posts):
        if p["id"] ==  id:
            return i

        


#EXAMPLE

@app.get("/") #Path operation /Route; a decorator applied to a function which acts like an end point of the api
def root():
    return {"message": "Hello World"}

#now we need to create a live server 
#Fastapi documentation under Tutorial-Userguide\First Steps\ liver server need to give a access point to server and app (FastAPI())
#go to terminal uvicorn (in installed libraries) main:app

#READ API-OPERATION 

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


#CREATE API-OPERATION 

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# #READ by ID API-operation

@app.get("/posts/{id}") #here the path parameter always return a string, that means id type is str
def get_post(id: int, response: Response): 
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return {'post_detail': post}

#DELETE operation

@app.delete("/posts/{id}")
def delete_post():
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#UPDATE OPERATION
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}