from typing import Optional, List
from pydantic import BaseModel


class Book(BaseModel):
    """Бизнес-сущность Книга"""
    id: Optional[int] = None
    title: str
    author: str
    year: int
    genre: str
    pages: int
    is_available: bool = True

    # Дополнительная информация
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None


class BookSearchResult(BaseModel):
    """Результат поиска книги"""
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    cover_url: Optional[str] = None
    source: str  # openlibrary
    external_id: Optional[str] = None


class BookDetails(BaseModel):
    """Детальная информация о книге"""
    title: str
    authors: List[str]
    publish_date: Optional[str] = None
    publishers: List[str]
    genres: List[str]
    isbn_10: List[str]
    isbn_13: List[str]
    pages: Optional[int] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None