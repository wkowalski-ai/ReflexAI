
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database.database import get_db
from ..schemas.user_schema import UserCreate, UserInDB
from ..schemas.token_schema import Token
from ..models.user_model import User
from ..security.hashing import get_password_hash, verify_password
from ..security.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Rejestruje nowego użytkownika"""
    # Sprawdź czy użytkownik już istnieje
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Utwórz nowego użytkownika
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        username=user_data.username
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Loguje użytkownika i zwraca token JWT"""
    # Znajdź użytkownika
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Sprawdź czy użytkownik istnieje i hasło jest poprawne
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Utwórz token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
