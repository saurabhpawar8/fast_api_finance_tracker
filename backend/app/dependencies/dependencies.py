from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import SessionLocal
from jose import jwt, JWTError
import os
from starlette import status
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def getCurrentUser(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "user_id": user_id}
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="COuld not validate user"
        )


db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(getCurrentUser)]
