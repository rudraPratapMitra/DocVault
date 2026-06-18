from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.auth import verify_access_token
from app.models.user import User



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
   
    email=verify_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    db_user=db.query(User).filter(User.email==email).first()
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return db_user