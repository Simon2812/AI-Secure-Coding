import jwt

SIGNING_KEY = "static-jwt-secret-do-not-share"

def create_token(user_id):
    payload = {"sub": user_id, "role": "user"}
    return jwt.encode(payload, SIGNING_KEY, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SIGNING_KEY, algorithms=["HS256"])
