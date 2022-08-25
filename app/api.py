
# In memory of Do Deeee

from datetime import date
import time
import os
import shutil
from fastapi import FastAPI, Depends, Query, Body, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from app.models import PostSchema, UserLoginSchema, UserSchema
from app.auth.auth_handler import sign_JWT
from app.auth.auth_bearer import JWTBearer
from supabase import create_client, Client
from pyuploadcare import Uploadcare
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="BayApp Developer API",
    description="This is an API for the BayApp. Contact dev at khizer.khan98@gmail.com for more information.",
    version="Alpha Pre Release 0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.environ.get("DB_URL")
key: str = os.environ.get("DB_KEY")

supabase: Client = create_client(url, key)


uploadcare = Uploadcare(public_key="f1f4d42015a1df04ce31", secret_key="a9492dac9132302f4360")


posts = [
    {
        "id" : 1,
        "title" : "Pancakes",
        "content" : "Lorem Ipsum"
    }
]


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
    #users.append(user)
    data = supabase.table("users").insert(user.dict()).execute()
    return sign_JWT(user.email)


@app.post('/user/login')
async def user_login(user : UserLoginSchema):
    if check_user(user):
        return sign_JWT(user.email)
    return {"error" : "Wrong credentials"}


def check_user(data : UserLoginSchema):
    
    db_users = supabase.table("users").select("*").execute()

    try:
        users_dict = db_users.dict()
        for user in users_dict["data"]:
            if user["email"] == data.email:
                if user["password"] == data.password:
                    return True
        return False
    
    except:
        return False


@app.post('/file')
async def upload_file(file: UploadFile = File(...)):
    
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_name = file.filename
    print(file_name)

    f_up = open(file_name, 'rb')
    ucare_file: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    return {"file_url" : str(ucare_file)}