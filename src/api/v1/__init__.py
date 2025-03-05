from fastapi import APIRouter

from . import auth, author, user

router = APIRouter(prefix="/api/v1")

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(author.router)
