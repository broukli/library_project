from ..use_case.entities import Book, BookDetails
from ..repository.books_repository import ExternalBookRepository


class BookEnrichmentService:
    """Сервис для обогащения данных книги"""

    def __init__(self, external_repo: ExternalBookRepository):
        self.external_repo = external_repo

    async def enrich_book_data(self, book: Book) -> Book:
        """Обогатить данные книги из внешних источников"""
        details = await self.external_repo.find_best_match(book.title, book.author)

        if not details:
            return book

        return self._merge_book_data(book, details)

    def _merge_book_data(self, book: Book, details: BookDetails) -> Book:
        """Объединить данные книги с внешней информацией"""
        enriched_book = book.model_copy()

        if not enriched_book.cover_url and details.cover_url:
            enriched_book.cover_url = details.cover_url

        if not enriched_book.description and details.description:
            enriched_book.description = details.description

        if not enriched_book.rating and details.rating:
            enriched_book.rating = details.rating

        if not enriched_book.isbn and details.isbn_13:
            enriched_book.isbn = details.isbn_13[0]
        elif not enriched_book.isbn and details.isbn_10:
            enriched_book.isbn = details.isbn_10[0]

        if not enriched_book.publisher and details.publishers:
            enriched_book.publisher = details.publishers[0]

        if not enriched_book.pages and details.pages:
            enriched_book.pages = details.pages

        return enriched_book