from fastapi import APIRouter

from . import auth, author, book, genre, user

router = APIRouter(prefix="/api/v1")

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(author.router)
router.include_router(book.router)
router.include_router(genre.router)
