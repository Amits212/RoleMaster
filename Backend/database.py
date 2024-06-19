from typing import List
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from models import User, Role

client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
roles_collection = db.roles
users_collection = db.users


async def create_role_in_db(role: Role):
    await roles_collection.insert_one(role.dict())


async def get_roles_from_db():
    cursor = roles_collection.find({})
    roles = await cursor.to_list(length=100)
    return [Role(**role) for role in roles]


async def get_user_from_db(user_id: str):
    user = await users_collection.find_one({"id": user_id})
    if user:
        return user
    else:
        return None

async def get_users_from_db():
    cursor = users_collection.find({})
    users = await cursor.to_list(length=100)
    return [User(**user) for user in users] if users else []


async def create_user_in_db(user: User):
    await users_collection.insert_one(user.dict())


async def update_user_in_db(user_id: str, user: User):
    result = await users_collection.update_one({"id": user_id}, {"$set": user.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return result

async def delete_user_from_db(user_id: str):
    result = await users_collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return result
