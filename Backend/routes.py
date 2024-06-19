from fastapi import APIRouter, Body, HTTPException, Depends, Request
from starlette import status

from models import User, Role, Permission
from database import (
    create_role_in_db,
    get_user_from_db,
    get_users_from_db,
    create_user_in_db,
    update_user_in_db,
    delete_user_from_db,
    get_roles_from_db,
)
from typing import List

router = APIRouter()

async def get_current_user(user_id: str) -> User:
    user = await get_user_from_db(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return User(**user)

async def check_permission(user: User, permission: Permission):
    if not user.has_permission(permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User '{user.username}' does not have permission '{permission.value}'"
        )

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
    await check_permission(current_user, Permission.READ)
    users = await get_users_from_db()
    return users

@router.post("/api/users")
async def create_user(user: User):
    await check_permission(current_user, Permission.ADD_USERS)
    await create_user_in_db(user=user)
    return {"message": "User created successfully"}


@router.put("/api/users/{user_id}")
async def update_user(user_id: int):
    await check_permission(current_user, Permission.WRITE)
    await update_user_in_db(user_id, user)
    return {"message": "User updated successfully"}

@router.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    await check_permission(current_user, Permission.DELETE)
    await delete_user_from_db(user_id)
    return {"message": "User deleted successfully"}


@router.api_route("/api/playground", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def playground(request: Request, current_user: User = Depends(get_current_user)):
    method_permission_map = {
        "GET": Permission.READ,
        "POST": Permission.ADD_USERS,
        "PUT": Permission.WRITE,
        "DELETE": Permission.DELETE,
        "PATCH": Permission.WRITE,
    }

    permission = method_permission_map.get(request.method)
    if permission:
        await check_permission(current_user, permission)
        return {
            "message": f"User '{current_user.username}' has '{permission.value}' permission for {request.method} method"}
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Method {request.method} not allowed"
        )

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
