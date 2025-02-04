import jwt
import datetime
from fastapi import HTTPException, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
app = FastAPI()

SECRET_KEY = "secret"  # Güvenlik için değiştirilebilir
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict):
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@app.post("/token")
def generate_token():
    return {"access_token": create_token({"user": "test_user"}), "token_type": "bearer"}

@app.get("/secure-data")
def secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": f"Hello, {payload['user']}!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
