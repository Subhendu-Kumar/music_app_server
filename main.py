import bcrypt
from prisma import Prisma
from schemas import UserCreate, UserLogin
from utils import hash_password, verify_password, create_access_token
from fastapi import FastAPI, HTTPException

app = FastAPI()
db = Prisma()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def entry():
    return {"message": "FastApi With Prisma & NeonDB"}


@app.post("/signup", status_code=201)
async def signup(user: UserCreate):
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
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/login", status_code=200)
async def login(user: UserLogin):
    db_user = await db.user.find_unique(where={"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token(data={"user_id": db_user.id, "email": db_user.email})
    return {"access_token": token, "message": "user loggedin successfully"}
