from typing import Any
from fastapi import FastAPI, HTTPException
import json

import src.homework.models as models
import src.homework.token as token
import src.homework.types as types
import src.homework.db_mock_methods as db


app = FastAPI()


@app.post("/registration")
async def registration(user: models.User):
    db_user = types.User(
        login=user.login,
        password=user.password,
        first_name=user.first_name,
        second_name=user.second_name,
        is_admin=False,
        skils=user.skils,
        company=user.company,
        posts_ids_to_names={},
    )
    user_id = db.add_user(db_user)
    jwt_token = token.make_token(user_id)
    return jwt_token


@app.post("/authorization")
async def authorization(user_info: models.UserInfo):
    user_token = user_info.token
    jwt_token = token.read_token(user_token)
    try:
        if token.is_token_need_refresh(user_token):
            user_id = jwt_token["user_id"]
            new_token = token.make_token(user_id)
        else:
            user_id = jwt_token["user_id"]
            new_token = user_token
    except token.BadToken:
        raise HTTPException(
            status_code=400, detail="Bad token, you are very suspicious"
        )
    user = db.find_user(user_id)
    if user.login != user_info.login:
        raise HTTPException(status_code=400, detail="Bad login")
    if user.password != hash(user_info.password):
        raise HTTPException(status_code=400, detail="Bad password")
    return new_token


async def get_token(user_token: str) -> Any:
    try:
        if token.is_token_need_refresh(user_token):
            raise HTTPException(status_code=400, detail="Bad token, you need relogin")
        return token.read_token(user_token)["user_id"]
    except token.BadToken:
        raise HTTPException(
            status_code=400, detail="Bad token, you are very suspicious"
        )


@app.post("/create_post")
async def create_post(post: models.CreateOrUpdatePost):
    user_id = await get_token(post.token)
    db_post = types.Post(
        name=post.name,
        text=post.text,
        author_id=user_id,
        tags=post.tags,
        comments=[],
        likes=0,
        dislikes=0,
    )
    post_id = db.add_or_update_post(db_post)
    db.add_post_id_to_user(post_id, user_id)


@app.post("/update_post")
async def update_post(post: models.CreateOrUpdatePost):
    user_id = await get_token(post.token)
    if post.post_id is None:
        raise HTTPException(status_code=400, detail="No post id")
    db_post = db.find_post(post.post_id, user_id)
    db_user = db.find_user(user_id)
    comments = db_post.comments
    for comment in post.new_comments:
        comments.append(types.Comment(user_id, db_user.first_name, comment))
    likes = db_post.likes
    if post.new_likes is not None:
        likes = post.new_likes
    dislikes = db_post.dislikes
    if post.new_dislikes is not None:
        dislikes = post.new_dislikes
    db_post = types.Post(
        name=post.name,
        text=post.text,
        author_id=user_id,
        tags=post.tags,
        comments=comments,
        likes=likes,
        dislikes=dislikes,
    )
    db.add_or_update_post(db_post)


@app.post("/delete_post")
async def delete_post(post: models.DeletePost):
    user_id = await get_token(post.token)
    db.delete_post(post.post_id, user_id)


@app.post("/get_posts")
async def get_posts(posts_info: models.GetPosts):
    with open("config.json", encoding="utf-8") as config:
        pagination_size = json.load(config)["pagination"]
    posts = db.get_posts(
        posts_info.author_id,
        posts_info.tags,
        posts_info.name_search,
        posts_info.pagination_current,
    )
    return {
        "posts": posts,
        "new_pagination": posts_info.pagination_current + pagination_size,
    }
