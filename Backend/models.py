from pydantic import BaseModel
from typing import List



class Role(BaseModel):
    id: int
    name: str

    def __str__(self):
        return f"Role: {self.name}"


class User(BaseModel):
    id: int
    name: str
    roles: List[Role]

    def __str__(self):
        return f"User: {self.name}"
