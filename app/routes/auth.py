from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.models.user import User
from app import schemas
from app.services import auth as auth_service

router = APIRouter()
logger = logging.getLogger(__name__)


def get_db():
    return auth_service.get_db()


@router.post("/login", response_model=schemas.Token)
async def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint that accepts JSON credentials
    """
    try:
        # Authenticate user
        user = auth_service.authenticate_user(db, credentials.username, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password"
            )
        
        # Create access token
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/login-form", response_model=schemas.Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint for form data (OAuth2 compatible)
    """
    try:
        user = auth_service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password"
            )
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login form error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        # Check if user already exists
        existing_user = auth_service.get_user(db, user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already registered"
            )
        
        # Create new user
        hashed_password = auth_service.get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/logout")
def logout(current_user: User = Depends(auth_service.get_current_user)):
    """
    Logout endpoint (client should discard token)
    """
    return {"message": "Logout successful"}


@router.get("/check-auth", response_model=schemas.User)
def check_auth(current_user: User = Depends(auth_service.get_current_user)):
    """
    Check if current user is authenticated
    """
    return current_user
