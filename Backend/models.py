from pydantic import BaseModel
from typing import List
from enum import Enum

class Permission(str, Enum):
    ADD_USERS = 'ADD_USERS'
    WRITE = 'WRITE'
    DELETE = 'DELETE'
    READ = 'READ'


class Role(BaseModel):
    id: int
    name: str
    permissions: List[Permission]

    def __str__(self):
        return f"Role: {self.name}"


class User(BaseModel):
    id: int
    username: str
    password: str
    role: Role

    def __str__(self):
        return f"User: {self.name}"

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.role.permissions
