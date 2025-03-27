from fastapi import APIRouter

from src.presentation.views.books_view import router as books_router
from src.presentation.views.borrow_view import router as borrow_router
from src.presentation.views.member_view import router as members_router
from src.presentation.views.return_view import router as return_router

router = APIRouter()

router.include_router(books_router, prefix="/books", tags=["Books"])
router.include_router(members_router, prefix="/members", tags=["Members"])
router.include_router(borrow_router, prefix="/borrow", tags=["Borrow"])
router.include_router(return_router, prefix="/return", tags=["Return"])
