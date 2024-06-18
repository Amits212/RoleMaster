from fastapi import APIRouter, Body, HTTPException
from starlette import status

from models import User, Role
from database import create_role_in_db, get_user_from_db, get_users_from_db, create_user_in_db
from typing import List

router = APIRouter()

@router.get("/api/roles")
async def get_all_roles():
    roles = await get_roles_from_db()
    return roles

@router.post("/api/roles")
async def create_role(role: Role):
    await create_role_in_db(role=role)
    return {"role": "Role created successfully"}


@router.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = await get_user_from_db(user_id=user_id)
    return user


@router.get("/api/users")
async def get_all_users():
    rooms = await get_users_from_db()
    return rooms


@router.post("/api/users")
async def create_user(user: User):
    await create_user_in_db(user=user)
    return {"user": "User created successfully"}

@router.post("/api/login")
async def login(user: User):
    user_in_db = await get_user_from_db(user_id=user.id)
    if user_in_db and user_in_db['password'] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


@router.post("/api/signup")
async def sign_up(user: User):
    user_in_db = await get_user_from_db(user_id=user.id)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    await create_user_in_db(user=user)
    return {"message": "User registered successfully"}
