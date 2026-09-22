from app.core.security import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.params import Depends
from app.api.dependencies import get_db
from app.core.config import settings

router = APIRouter()

def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid login or password')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({'sub': user.email}, access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post("/token")
def token(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
                           ):
    return login_for_access_token(form_data, db)