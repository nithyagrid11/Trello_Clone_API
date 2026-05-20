from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.board import Board
from app.schemas.user import UserCreate, UserResponse
from app.utils.password import hash_password
from app.schemas.user import UserLogin, Token
from app.utils.password import verify_password
from app.utils.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    valid_password = verify_password(
        form_data.password,
        user.password
    )
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }