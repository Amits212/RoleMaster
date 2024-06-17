from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from models import User, Role

client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
roles_collection = db.roles
users_collection = db.users


async def create_role(role: Role):
    await roles_collection.insert_one(role.dict())


async def get_roles():
    cursor = roles_collection.find({})
    roles = await cursor.to_list(length=100)
    return [Role(**role) for role in roles]


async def get_user(user_id: str):
    user = await users_collection.find_one({"id": user_id})
    if user:
        return user
    else:
        return None

async def get_all_users():
    cursor = users_collection.find({})
    users = await cursor.to_list(length=100)
    return [User(**user) for user in users]


async def create_user(user: User):
    await users_collection.insert_one(user.dict())
