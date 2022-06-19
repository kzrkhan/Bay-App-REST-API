
# In memory of Do Deeee

from datetime import date
import os
from fastapi import FastAPI, Depends, Query, Body
from pydantic import BaseModel
from typing import Optional
from app.models import PostSchema, UserLoginSchema, UserSchema
from app.auth.auth_handler import sign_JWT
from app.auth.auth_bearer import JWTBearer


app = FastAPI(
    title="BayApp Developer API",
    description="This is an API for the BayApp. Contact dev at khizer.khan98@gmail.com for more information.",
    version="Alpha Pre Release 0.1"
)


posts = [
    {
        "id" : 1,
        "title" : "Pancakes",
        "content" : "Lorem Ipsum"
    }
]


users = []


@app.get("/")
async def read_items():
    return {'msg': 'Hello'}


@app.get('/posts')
async def get_posts():
    return {'data' : posts}


@app.get('/posts/{id}')
async def get_single_post(id:int):
    if id > len(posts):
        return {'error' : 'No post with supplied ID'}
    else:
        for post in posts:
            if post["id"] == id:
                return {'data' : post
                }


@app.post('/add_post', dependencies=[Depends(JWTBearer())])
async def add_post(post:PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())

    return {'data' : 'post added'}


@app.post('/user/signup')
async def create_user(user : UserSchema):
    users.append(user)
    return sign_JWT(user.email)


@app.post('/user/login')
async def user_login(user : UserLoginSchema):
    if check_user(user):
        return sign_JWT(user.email)
    return {"error" : "Wrong credentials"}


def check_user(data : UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False