from abc import ABC, abstractmethod
from typing import List, Optional
from ..use_case.entities import Book, BookSearchResult, BookDetails


class BookRepository(ABC):
    """Абстракция репозитория для работы с книгами"""

    @abstractmethod
    async def get_all(self) -> List[Book]:
        """Получить все книги"""
        pass

    @abstractmethod
    async def get_by_id(self, book_id: int) -> Optional[Book]:
        """Получить книгу по ID"""
        pass

    @abstractmethod
    async def create(self, book: Book) -> Book:
        """Создать новую книгу"""
        pass

    @abstractmethod
    async def update(self, book_id: int, book: Book) -> Optional[Book]:
        """Обновить книгу"""
        pass

    @abstractmethod
    async def delete(self, book_id: int) -> bool:
        """Удалить книгу"""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Book]:
        """Поиск книг в локальном хранилище"""
        pass


class ExternalBookRepository(ABC):
    """Абстракция репозитория для работы с внешними источниками книг"""

    @abstractmethod
    async def search_books(self, query: str, limit: int) -> List[BookSearchResult]:
        """Поиск книг во внешних источниках"""
        pass

    @abstractmethod
    async def get_book_details(self, external_id: str) -> Optional[BookDetails]:
        """Получить детальную информацию о книге"""
        pass

    @abstractmethod
    async def find_best_match(self, title: str, author: str) -> Optional[BookDetails]:
        """Найти наилучшее совпадение для книги"""
        pass