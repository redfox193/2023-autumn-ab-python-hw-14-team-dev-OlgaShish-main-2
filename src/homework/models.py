from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel
from src.homework.types import Tags


class User(BaseModel):
    login: str
    password: str
    first_name: str
    second_name: str
    skils: list[str]
    company: Optional[str]


class UserInfo(BaseModel):
    login: str
    password: str
    token: str


class CreateOrUpdatePost(BaseModel):
    post_id: Optional[Any]
    name: str
    text: str
    tags: list[Tags]
    token: str
    new_likes: Optional[int]
    new_dislikes: Optional[int]
    new_comments: list[str]


class GetPosts(BaseModel):
    author_id: Optional[Any]
    tags: list[Tags]
    name_search: Optional[str]
    pagination_current: int


class DeletePost(BaseModel):
    post_id: Any
    token: str
