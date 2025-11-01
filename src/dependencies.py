from fastapi import Depends
from .database.repositories import PostgreSQLBookRepository
from .clients_api import ExternalBookAggregator
from .use_case.book_use_cases import BookUseCases
from .repository.books_repository import BookRepository, ExternalBookRepository

def get_book_repository() -> BookRepository:
    """Зависимость для репозитория книг"""
    return PostgreSQLBookRepository()

def get_external_repository() -> ExternalBookRepository:
    """Зависимость для внешнего репозитория"""
    return ExternalBookAggregator()

def get_book_use_cases(
    book_repo: BookRepository = Depends(get_book_repository),
    external_repo: ExternalBookRepository = Depends(get_external_repository)
) -> BookUseCases:
    """Зависимость для сценариев использования книг"""
    return BookUseCases(book_repo, external_repo)