import time
from typing import Dict
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


#def token_response(token: str):
 #   return {
  #      "access_token": token
   # }

def sign_JWT(user_id : str):
    payload = {
        "user_id" : user_id,
        "expired" : time.time() + 6000
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def decode_JWT(token : str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expired"] >= time.time() else None
    except:
        return {}