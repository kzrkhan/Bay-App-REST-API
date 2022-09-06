
# In memory of Do Deeee

from datetime import date
import time
import os
import shutil
from fastapi import FastAPI, Depends, Query, Body, UploadFile, File, Form
from pydantic import BaseModel, EmailStr
from typing import Optional

from pyparsing import Char
from app.models import PostSchema, UserLoginSchema, UserSchema
from app.auth.auth_handler import sign_JWT
from app.auth.auth_bearer import JWTBearer
from supabase import create_client, Client
from pyuploadcare import Uploadcare
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import geodesic


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
async def root_endpoint():
    return {'response': 'Bay App Developer API root endpoint'}


@app.post('/user/signup')
async def create_user(user : UserSchema):
    #users.append(user)
    if check_existing_email(user):
        return {"response" : "A user with same email already exists"}
    else:
        data = supabase.table("users").insert(user.dict()).execute()
        print()
        uid = ((((data.dict())["data"])[0])["id"])
        return {
        "uid" : uid,
        "email" : user.email,
        "name" : user.first_name,
        "token" : sign_JWT(user.email)
        }


@app.post('/user/login')
async def user_login(user : UserLoginSchema):
    if check_user(user):
        db_users = supabase.table("users").select("id, email, first_name").execute()
        db_data = db_users.dict()
        for data in db_data["data"]:
            if data["email"] == user.email:
                f_name = data["first_name"]
                uid = data["id"]
        return {
        "uid" : uid,
        "email" : user.email,
        "name" : f_name,
        "token" : sign_JWT(user.email)
        }
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


def check_existing_email(data : UserLoginSchema):
    
    db_users = supabase.table("users").select("*").execute()

    try:
        users_dict = db_users.dict()
        for user in users_dict["data"]:
            if user["email"] == data.email:
                return True
        return False
    
    except:
        return False


@app.post('/report')
async def issue_report(issue: str = Form(...), media: UploadFile = File(...), reported_by: str = Form(...)):
    
    with open(f'{media.filename}', 'wb') as buffer:
        shutil.copyfileobj(media.file, buffer)

    file_name = media.filename

    f_up = open(file_name, 'rb')
    media_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass
    
    report = {
        "issue" : issue,
        "media" : str(media_url),
        "reported_by" : reported_by
    }

    try:
        supabase.table("reports").insert(report).execute()
    except:
        return {"response" : "Error in DB Transaction"}
    
    return {"response" : "success"}


@app.get('/getreports', dependencies=[Depends(JWTBearer())])
async def get_reports():
    
    try:
        report_data = supabase.table("reports").select("*").execute()
    except:
        return {"response" : "Error in DB Transaction"}
    
    return report_data


@app.post('/addpoi')
async def add_poi(name: str = Form(...), description: str = Form(...), logo: UploadFile = File(...), title_image: UploadFile = File(...), rating: int = Form(...), img_1: UploadFile = File(...), img_2: UploadFile = File(...), img_3: UploadFile = File(...), img_4: UploadFile = File(...), img_5: UploadFile = File(...), beach_id: int = Form(...)):
    
    with open(f'{logo.filename}', 'wb') as buffer:
        shutil.copyfileobj(logo.file, buffer)

    file_name = logo.filename

    f_up = open(file_name, 'rb')
    logo_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{title_image.filename}', 'wb') as buffer:
        shutil.copyfileobj(title_image.file, buffer)

    file_name = title_image.filename

    f_up = open(file_name, 'rb')
    title_image_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{img_1.filename}', 'wb') as buffer:
        shutil.copyfileobj(img_1.file, buffer)

    file_name = img_1.filename

    f_up = open(file_name, 'rb')
    img_1_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{img_2.filename}', 'wb') as buffer:
        shutil.copyfileobj(img_2.file, buffer)

    file_name = img_2.filename

    f_up = open(file_name, 'rb')
    img_2_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{img_3.filename}', 'wb') as buffer:
        shutil.copyfileobj(img_3.file, buffer)

    file_name = img_3.filename

    f_up = open(file_name, 'rb')
    img_3_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{img_4.filename}', 'wb') as buffer:
        shutil.copyfileobj(img_4.file, buffer)

    file_name = img_4.filename

    f_up = open(file_name, 'rb')
    img_4_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass

    with open(f'{img_5.filename}', 'wb') as buffer:
        shutil.copyfileobj(img_5.file, buffer)

    file_name = img_5.filename

    f_up = open(file_name, 'rb')
    img_5_url: File = uploadcare.upload(f_up)
    f_up.close()

    try:
        os.remove(file_name)
    except:
        pass


    poi_data = {
        "name" : name,
        "description" : description,
        "logo" : str(logo_url),
        "title_image" : str(title_image_url),
        "rating" : rating,
        "img_1" : str(img_1_url),
        "img_2" : str(img_2_url),
        "img_3" : str(img_3_url),
        "img_4" : str(img_4_url),
        "img_5" : str(img_5_url),
        "beach_id" : beach_id
    }

    supabase.table("poi").insert(poi_data).execute()

    return {"response" : "success"}


@app.get('/nearbypoi/{beach_id}', dependencies=[Depends(JWTBearer())])
async def get_nearby_poi(beach_id:int):
    try:
        poi_data = supabase.table("poi").select("*").eq("beach_id",beach_id).execute()
    except:
        return {"response" : "Error occurred in DB Transaction"}
    return poi_data 


@app.get('/nearbybeach/{lat},{lon}', dependencies=[Depends(JWTBearer())])
async def get_nearby_beach(lat:float, lon:float):

    beach_data = ((supabase.table("beaches").select("id, name, lat, lon").execute()).dict())["data"]

    distance_list = []

    for data in beach_data:
        beach_point = (data["lat"] , data["lon"])
        user_point = (lat , lon)
        distance = geodesic(beach_point, user_point).kilometers
        distance_list.append(distance)
    
    nearby_beach_index = distance_list.index(min(distance_list))

    return beach_data[nearby_beach_index]


@app.post('/updatehelper/{email},{status}', dependencies=[Depends(JWTBearer())])
async def update_helper_status(email:str, status:bool):

    query_result = supabase.table("users").select("id, email").execute()
    db_data = (query_result.dict())["data"]

    print("parameter email: ", email)

    for data in db_data:
        print("db email: ",data["email"])
        if str(data["email"]) == str(email):
            id = int(data["id"])
            try:
                supabase.table("users").update({"helper":status}).eq("id",id).execute()
            except:
                return {"response" : "Error in DB Transaction"}

            return {"response" : "Status updated successfully"}
    
    return {"response" : "Error in DB Transaction"}


@app.post('/updatelocation/{uid},{email},{lat},{lon}')
async def update_location_coordinates(uid:int, email:str, lat:float, lon:float):
    
    try:
        data = supabase.table("live locations").select("*").eq("user_id",uid).execute()
        db_dict = data.dict()
        if len(db_dict["data"]) == 0:
            try:
                supabase.table("live locations").insert({"user_id":uid , "email":email , "lat":lat , "lon":lon}).execute()
            except:
                return {"response" : "Error in DB Transaction"}
        else:
            try:
                supabase.table("live locations").update({"lat":lat , "lon":lon}).eq("user_id",uid).execute()
            except:
                return {"response" : "Error in DB Transaction"}
    except:
        return {"response" : "Error in DB Transaction"}
    
    return {"response" : "Updated"}


@app.post('/sos/start/{uid},{lat},{lon}', dependencies=[Depends(JWTBearer())])
async def start_sos(uid:int, lat:float, lon:float):
    
    try:
        insertion_response = supabase.table("sos transaction record").insert({"init_id":uid}).execute()
    except:
        return {"response" : "Error in DB Transaction"}

    try:
        helper_data = supabase.table("users").select("id").eq("helper",True).execute()
    except:
        return {"response" : "Error occured in DB Transaction"}

    try:
        location_data = supabase.table("live locations").select("user_id, lat, lon").execute()
    except:
        return {"response" : "Error occured in DB transaction"}

    helper_dict = (helper_data.dict())["data"]

    location_dict = (location_data.dict())["data"]

    distance_dict = {}

    user_point = (lat, lon)

    for helper in helper_dict:
        for location_data in location_dict:
            if helper["id"] == location_data["user_id"]:
                helper_point = (location_data["lat"], location_data["lon"])
                distance = geodesic(helper_point, user_point).kilometers
                distance_dict[helper["id"]] = distance

    '''lowest_distance = 10000
    target_id = 0
    for id in distance_dict.keys():
        if distance_dict[id] < lowest_distance:
            lowest_distance = distance_dict[id]
            target_id = id
    
    distance_sorted = sorted(distance_dict.items(), key=lambda kv:
                 (kv[1], kv[0]))


    sos_transaction_id = (((insertion_response.dict())["data"])[0])["id"]
    
    try:
        responder_update_response = supabase.table("sos transaction record").update({"resp_id":target_id}).eq("id",sos_transaction_id).execute()
    except:
        return {"response" : "Error in DB Transaction"}

    responder_data = ((((supabase.table("users").select("first_name","last_name").eq("id",target_id).execute()).dict())["data"])[0])

    responder_eta = (60.0*lowest_distance)/4.0

    api_response = {
        "first_name" : responder_data["first_name"],
        "last_name" : responder_data["last_name"],

    }

    print(api_response)'''


@app.get('/help_needed/{uid}', dependencies=[Depends(JWTBearer())])
async def help_needed():
    pass