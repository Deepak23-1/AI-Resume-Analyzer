from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.utils.oauth2 import oauth_scheme
from app.utils.jwt_handler import verify_access_token
from fastapi import HTTPException, status




def get_current_user(
        token: str = Depends(oauth_scheme),
        db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    db_user = db.query(User).filter(User.email==email).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found" 
        )
    
    return db_user