#responsible for signing,encoding, decoding ans returning JWTs.
import time
import jwt
from decouple import config

jwt_secret = config("secret")
jwt_algorithm = config("algorithm")


def token_response(token: str):
    return {
        "access token": token
    }

def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600 
    }
    token = jwt.encode(payload,jwt_secret,algorithm=jwt_algorithm)
    return token_response(token)

def decodeJWT(token: str):
    try:    
        decoded_token = jwt.decode(token,jwt_secret,algorithm=jwt_algorithm)
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}