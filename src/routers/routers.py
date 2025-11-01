from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..use_case.book_use_cases import BookUseCases
from ..schemas.DTO import CreateBookCommand, UpdateBookCommand
from ..dependencies import get_book_use_cases
from ..schemas.shemas import (
    BookCreateSchema, BookUpdateSchema, BookResponseSchema,
    SearchResponseSchema, ExternalSearchResponseSchema
)

router = APIRouter(prefix="/books", tags=["Книги"])

@router.get("/", response_model=List[BookResponseSchema])
async def get_books(
    use_cases: BookUseCases = Depends(get_book_use_cases)
):
    """Получить все книги"""
    books = await use_cases.get_all_books()
    return books

@router.get("/{book_id}", response_model=BookResponseSchema)
async def get_book(book_id: int,use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Получить книгу по ID"""
    book = await use_cases.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.post("/", response_model=BookResponseSchema)
async def create_book(book_data: BookCreateSchema,use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Создать новую книгу"""
    command = CreateBookCommand(**book_data.model_dump())
    book = await use_cases.create_book(command)
    return book

@router.put("/{book_id}", response_model=BookResponseSchema)
async def update_book(book_id: int,book_data: BookUpdateSchema,use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Обновить книгу"""
    command = UpdateBookCommand(**book_data.model_dump(exclude_unset=True))
    book = await use_cases.update_book(book_id, command)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Удалить книгу"""
    deleted = await use_cases.delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

@router.get("/search/internal", response_model=SearchResponseSchema)
async def search_books(query: str,use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Поиск книг в локальной базе"""
    books = await use_cases.search_books(query)
    return SearchResponseSchema(query=query, results=books)

@router.get("/search/external", response_model=ExternalSearchResponseSchema)
async def search_external_books(query: str,limit: int = 10,use_cases: BookUseCases = Depends(get_book_use_cases)):
    """Поиск книг во внешних источниках"""
    results = await use_cases.search_external_books(query, limit)
    return ExternalSearchResponseSchema(query=query, results=results)