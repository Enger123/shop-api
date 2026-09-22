from fastapi.params import Depends
from typing import Annotated
from app.core.security import oauth_2_scheme, get_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user import UserService
from fastapi import HTTPException
from jose import jwt, JWTError
from app.core.config import settings


def get_current_user(token: str=Depends(oauth_2_scheme), db: Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=401, detail='Invalid login or password')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = get_user(username, db)
    if user is None:
        raise credential_exception
    return user

Current_user = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[Session, Depends(get_db)]

def get_user_service(db: DBSession):
    return UserService(db)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
