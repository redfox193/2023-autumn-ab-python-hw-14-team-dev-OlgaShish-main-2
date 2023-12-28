from enum import Enum
from datetime import datetime
from typing import Any, Optional

class Tags(Enum):
    PROGRAMMING = 1
    PYTHON = 2
    BACKEND = 3
    EDUCATION = 4
    TESTS = 5
    CTHULHU = 6


class Comment:
    def __init__(self, user_id: Any, user_name, text: str) -> None:
        self.comment_id = None
        self.user_id = user_id
        self.user_name = user_name
        self.text = text
        self.time = datetime.now()


class Post:
    def __init__(
        self,
        name: str,
        text: str,
        author_id: Any,
        tags: list[Tags],
        comments: list[Comment],
        likes: int,
        dislikes: int,
    ) -> None:
        self.post_id = None
        self.name = name
        self.text = text
        self.author_id = author_id
        self.tags = tags
        self.comments = comments
        self.likes = likes
        self.dislikes = dislikes
        self.time = datetime.now()


class User:
    def __init__(
        self,
        login: str,
        password: str,
        first_name: str,
        second_name: str,
        is_admin: bool,
        skils: list[str],
        company: Optional[str],
        posts_ids_to_names: dict[str, str],
    ) -> None:
        self.user_id = None
        self.login = login
        self.password = hash(password)
        self.first_name = first_name
        self.second_name = second_name
        self.is_admin = is_admin
        self.skils = skils
        self.company = company
        self.posts_ids_to_names = posts_ids_to_names
