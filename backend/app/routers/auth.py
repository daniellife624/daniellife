from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import verify_password, hash_password, create_access_token
from ..config import settings
from ..models.user import User
from ..schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()

    # Fallback: accept .env credentials even if DB has no users
    if not user:
        if body.email == settings.ADMIN_EMAIL and body.password == settings.ADMIN_PASSWORD:
            token = create_access_token(subject=body.email)
            return TokenResponse(access_token=token, name="Daniel", email=body.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, name=user.name, email=user.email)


@router.post("/register", response_model=TokenResponse, include_in_schema=False)
def register(body: LoginRequest, name: str = "Daniel", db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=name, email=body.email, hashed_password=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, name=user.name, email=user.email)
