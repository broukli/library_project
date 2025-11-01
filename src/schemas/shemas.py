from pydantic import BaseModel
from typing import Optional, List


class BookCreateSchema(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    is_available: bool = True
    cover_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    is_available: Optional[bool] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None

class BookResponseSchema(BaseModel):
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


class SearchResponseSchema(BaseModel):
    query: str
    results: List[BookResponseSchema]

class ExternalSearchResponseSchema(BaseModel):
    query: str
    results: List[dict]  # Упрощенная схема для внешних результатов