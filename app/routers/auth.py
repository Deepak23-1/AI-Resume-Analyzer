from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.database.database import get_db
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]

)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "message": "User registered successfully",
        "user_id": new_user.id
    }



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db: Session=Depends(get_db)
):
    db_user=db.query(User).filter(User.email==form_data.username).first()

    if db_user is None:
        return {"message": "Invalid email or password"}
    
    if not verify_password(form_data.password, db_user.password):
        return{"message": "Ivalid email or password"}
    
    access_token = create_access_token(data={"sub": db_user.email})
    
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.get("/profile")
def profile(current_user: User=Depends(get_current_user)):
    return{
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }