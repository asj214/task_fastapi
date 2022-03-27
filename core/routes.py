from fastapi import APIRouter
from apps import posts, companies


router = APIRouter()
router.include_router(posts.router, tags=['posts'])
router.include_router(companies.router, tags=['companies'])