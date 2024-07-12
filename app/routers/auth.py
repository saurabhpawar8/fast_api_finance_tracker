from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.dependencies.dependencies import db_dependecy
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import jwt

from fastapi.responses import JSONResponse


from app.models.schema import User

# from core.dependencies import SECRET_KEY, ALGORITHM, bcryptContext

router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/signup")
async def signUp(db: db_dependecy, userRequest: CreateUserRequest):
    username = userRequest.email.split("@", 1)[0]
    user = User(
        email=userRequest.email,
        password=bcrypt_context.hash(userRequest.password),
        username=username,
    )
    db.add(user)
    db.commit()
    return JSONResponse({"message": "User created with {username}"})


def authenticateUser(username: str, password: str, db: db_dependecy):
    user = db.query(User).filter(User.username == username).first()
    print(user)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False

    return user


def createAccessToken(username: str, userId: int, expiresDelta: timedelta):
    encode = {"sub": username, "id": userId}
    expires = datetime.now() + expiresDelta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependecy
):
    user = authenticateUser(form_data.username, form_data.password, db)
    print(user)
    if not user:
        return JSONResponse({"Error": "Not Authenticated"})
    token = createAccessToken(user.username, user.id, timedelta(minutes=20))
    return JSONResponse(
        {"access_token": token, "token_type": "bearer", "message": "Login successful"}
    )



