from typing import List, Optional
from .entities import Book, BookSearchResult
from ..repository.books_repository import BookRepository, ExternalBookRepository
from ..services.enrichment import BookEnrichmentService
from ..schemas.DTO import CreateBookCommand, UpdateBookCommand


class BookUseCases:
    """Сценарии использования для работы с книгами"""

    def __init__(
            self,
            book_repo: BookRepository,
            external_repo: ExternalBookRepository
    ):
        self.book_repo = book_repo
        self.external_repo = external_repo
        self.enrichment_service = BookEnrichmentService(external_repo)

    async def get_all_books(self) -> List[Book]:
        """Получить все книги"""
        return await self.book_repo.get_all()

    async def get_book(self, book_id: int) -> Optional[Book]:
        """Получить книгу по ID"""
        return await self.book_repo.get_by_id(book_id)

    async def create_book(self, command: CreateBookCommand) -> Book:
        """Создать новую книгу"""
        book = Book(**command.model_dump())

        # Обогащаем данные из внешних источников
        enriched_book = await self.enrichment_service.enrich_book_data(book)

        return await self.book_repo.create(enriched_book)

    async def update_book(self, book_id: int, command: UpdateBookCommand) -> Optional[Book]:
        """Обновить книгу"""
        existing_book = await self.book_repo.get_by_id(book_id)
        if not existing_book:
            return None

        # Обновляем только переданные поля
        update_data = command.model_dump(exclude_unset=True)
        updated_book = existing_book.model_copy(update=update_data)

        return await self.book_repo.update(book_id, updated_book)

    async def delete_book(self, book_id: int) -> bool:
        """Удалить книгу"""
        return await self.book_repo.delete(book_id)

    async def search_books(self, query: str) -> List[Book]:
        """Поиск книг в локальном хранилище"""
        return await self.book_repo.search(query)

    async def search_external_books(self, query: str, limit: int = 10) -> List[BookSearchResult]:
        """Поиск книг во внешних источниках"""
        return await self.external_repo.search_books(query, limit)
