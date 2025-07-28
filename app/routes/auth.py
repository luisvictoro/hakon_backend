from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import User
from app import schemas
from app.services import auth as auth_service

router = APIRouter()


def get_db():
    return auth_service.get_db()


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(current_user: User = Depends(auth_service.get_current_user)):
    return {"message": "Logout successful"}


@router.get("/check-auth", response_model=schemas.User)
def check_auth(current_user: User = Depends(auth_service.get_current_user)):
    return current_user
