from src.homework.types import User, Post, Tags
from typing import Any, Optional


def add_user(user: User) -> Any:
    """add user into db"""


def find_user(user_id: Any) -> User:
    """check is user into db"""
    pass


def add_or_update_post(post: Post) -> Any:
    """add post into db"""


def find_post(post_id: Any, user_id: Any) -> Post:
    """find post by user_id and post_id"""


def add_post_id_to_user(post_id: Any, user_id: Any) -> None:
    """add post_id to user_id"""


def get_posts(
    author_id: Any, tags: list[Tags], name_search: Optional[str], pagination: int
) -> list[Post]:
    """get_posts"""


def delete_post(post_id: Any, user_id: Any) -> None:
    """delete_post"""
