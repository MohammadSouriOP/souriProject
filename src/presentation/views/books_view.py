from typing import List

from fastapi import APIRouter, Body, HTTPException

from src.application.books_services import BooksService
from src.domain.books_entity import BookEntity
from src.domain.models.book_model import BookModel

router = APIRouter()
service = BooksService()


@router.get("/", response_model=List[BookModel])
def get_books():
    books = service.get_all()
    return [book.to_model() for book in books]


@router.get("/{book_id}", response_model=BookModel)
def get_book(book_id: int):
    book = service.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_model()


@router.post("/", response_model=BookModel, status_code=201)
def create_book(data: dict = Body(...)):
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        raise HTTPException(status_code=400, detail="Missing title or author")

    ent = BookEntity(title=title, author=author)
    result = service.add(ent)
    if result:
        return result.to_model()
    raise HTTPException(status_code=500, detail="Error adding book")


@router.put("/{book_id}", response_model=dict)
@router.patch("/{book_id}", response_model=dict)
def update_book(book_id: int, data: dict = Body(...)):
    result = service.update(book_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully"}


@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int):
    result = service.delete(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
