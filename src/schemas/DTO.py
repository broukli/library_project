from pydantic import BaseModel
from typing import Optional

class CreateBookCommand(BaseModel):
    """DTO для создания книги"""
    title: str
    author: str
    year: int
    genre: str
    pages: int
    is_available: bool = True
    cover_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class UpdateBookCommand(BaseModel):
    """DTO для обновления книги"""
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    is_available: Optional[bool] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class BookResponse(BaseModel):
    """DTO для ответа с книгой"""
    id: int
    title: str
    author: str
    year: int
    genre: str
    pages: int
    is_available: bool
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None

class SearchBooksQuery(BaseModel):
    """DTO для поиска книг"""
    query: str
    limit: int = 10