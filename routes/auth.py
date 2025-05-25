from utils.database_util import get_db
from schemas.auth import UserCreate, UserLogin
from utils.jwt_util import create_access_token
from fastapi import APIRouter, HTTPException, Depends
from utils.password_util import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=201)
async def signup(user: UserCreate, db = Depends(get_db)):
    try:
        existing_user = await db.user.find_unique(where={"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(user.password)
        created_user = await db.user.create(
            data={
                "name": user.name,
                "email": user.email,
                "password": hashed_password,
            }
        )
        if not created_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        return {
            "id": created_user.id,
            "name": created_user.name,
            "email": created_user.email,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login", status_code=200)
async def login(user: UserLogin, db = Depends(get_db)):
    try:
        db_user = await db.user.find_unique(where={"email": user.email})
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        token = create_access_token(data={"user": {"id": db_user.id, "email": db_user.email}})
        return {"access_token": token, "message": "User logged in successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")