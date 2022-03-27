from typing import List
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from models import Post, Post_Pydantic, PostIn_Pydantic


router = APIRouter(prefix='/posts')

@router.get('', name='post.list', response_model=List[Post_Pydantic])
async def post_list(page: int = 1, per_page: int = 20):
    offset = (page - 1) * per_page
    return await Post_Pydantic.from_queryset(Post.all().offset(offset).limit(per_page))


@router.post('', response_model=Post_Pydantic, status_code=HTTP_201_CREATED)
async def post_create(post: PostIn_Pydantic):
    obj = await Post.create(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_tortoise_orm(obj)


@router.get('/{id}', response_model=Post_Pydantic)
async def post_show(id: int):
    return await Post_Pydantic.from_queryset_single(Post.get(id=id))


@router.delete('/{id}')
async def post_remove(id: int):
    await Post.get(id=id).delete()
    return Response(status_code=HTTP_204_NO_CONTENT)
