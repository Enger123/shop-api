from fastapi.params import Depends
from typing import Annotated
from app.core.security import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user import UserService


Current_user = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[Session, Depends(get_db)]

def get_user_service(db: DBSession):
    return UserService(db)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
