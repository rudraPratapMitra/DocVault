from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.core.auth import create_access_token, verify_access_token
from app.core.oauth2 import get_current_user

router=APIRouter()
@router.post("/register")
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    hashed_password =hash_password(user.password)
    new_user=User(
        email=user.email,
        hashed_password=hashed_password
        )
    existingUser=(
        db.query(User).filter(User.email==user.email).first()
    )
    if existingUser:
        raise HTTPException(
            status_code=400,
            detail="User Already Registerd"
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "id":new_user.id,
        "email":new_user.email
    }

@router.post("/login")
def login_user(user:UserLogin,db:Session=Depends(get_db)):
    email=user.email
    password=user.password

    db_user=db.query(User).filter(User.email==email).first()
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Auntehntication Failed"
        )
    hashed_password=db_user.hashed_password
    token = create_access_token(
        data={"sub": db_user.email}
    )
    if verify_password(password,hashed_password):
       return {
        "access_token": token,
        "token_type": "bearer"
    }
    else:
        raise HTTPException(
            status_code=401,
            detail="Auntehntication Failed"
        )
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
