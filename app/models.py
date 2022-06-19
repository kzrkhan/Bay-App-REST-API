from pydantic import BaseModel, EmailStr, Field
import datetime

class BaseUser (BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    dob: datetime.date
    age: int
    helper: bool

class PostSchema (BaseModel):
    id : int = Field(default=None)
    title : str = Field(...)
    content : str = Field(...)

class UserSchema (BaseModel):
    fullname : str
    email : EmailStr
    password : str

class UserLoginSchema (BaseModel):
    email : EmailStr
    password : str
