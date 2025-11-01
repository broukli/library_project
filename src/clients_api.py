# infrastructure/api/clients.py
import httpx
from typing import List, Optional, Dict, Any
from .use_case.entities import BookSearchResult, BookDetails
from .repository.books_repository import ExternalBookRepository
from .database.settings import settings


class OpenLibraryClient(ExternalBookRepository):
    """Клиент для Open Library API"""

    def __init__(self):
        self.base_url = settings.api.open_library_base_url
        self.timeout = settings.api.request_timeout

    async def search_books(self, query: str, limit: int = 10) -> List[BookSearchResult]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/search.json",
                    params={"q": query, "limit": limit}
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for doc in data.get("docs", [])[:limit]:
                    results.append(BookSearchResult(
                        title=doc.get("title", "Unknown Title"),
                        author=doc.get("author_name", ["Unknown"])[0],
                        year=doc.get("first_publish_year"),
                        isbn=doc.get("isbn", [""])[0] if doc.get("isbn") else None,
                        cover_url=self._get_cover_url(doc.get("cover_i")),
                        source="openlibrary",
                        external_id=doc.get("key")
                    ))

                return results
        except Exception as e:
            print(f"OpenLibrary error: {e}")
            return []

    async def get_book_details(self, external_id: str) -> Optional[BookDetails]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}{external_id}.json")
                response.raise_for_status()
                data = response.json()

                return BookDetails(
                    title=data.get("title", "Unknown Title"),
                    authors=self._extract_authors(data.get("authors", [])),
                    publish_date=data.get("first_publish_date"),
                    publishers=[],
                    genres=data.get("subjects", [])[:5],
                    isbn_10=[],
                    isbn_13=[],
                    pages=None,
                    cover_url=None,
                    description=self._extract_description(data.get("description")),
                    rating=self._extract_rating(data.get("ratings_summary"))
                )
        except Exception as e:
            print(f"OpenLibrary details error: {e}")
            return None

    async def find_best_match(self, title: str, author: str) -> Optional[BookDetails]:
        search_results = await self.search_books(f"{title} {author}", limit=1)
        if search_results and search_results[0].external_id:
            return await self.get_book_details(search_results[0].external_id)
        return None

    def _get_cover_url(self, cover_id: Optional[int]) -> Optional[str]:
        if not cover_id:
            return None
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

    def _extract_authors(self, authors_data: List[Dict]) -> List[str]:
        authors = []
        for author in authors_data:
            if isinstance(author, dict) and 'name' in author:
                authors.append(author['name'])
        return authors

    def _extract_description(self, description_data: Any) -> Optional[str]:
        if not description_data:
            return None
        if isinstance(description_data, dict):
            return description_data.get('value')
        return str(description_data)

    def _extract_rating(self, ratings_data: Dict) -> Optional[float]:
        if ratings_data and 'average' in ratings_data:
            return round(ratings_data['average'], 2)
        return None


class ExternalBookAggregator(ExternalBookRepository):
    """Агрегатор данных из нескольких внешних источников"""

    def __init__(self):
        self.clients: List[ExternalBookRepository] = [
            OpenLibraryClient(),
            # Можно добавить другие клиенты (Google Books и т.д.)
        ]

    async def search_books(self, query: str, limit: int = 10) -> List[BookSearchResult]:
        all_results = []
        for client in self.clients:
            try:
                results = await client.search_books(query, limit)
                all_results.extend(results)
            except Exception as e:
                print(f"Error in {client.__class__.__name__}: {e}")
                continue

        # Убираем дубликаты
        return self._deduplicate_results(all_results)[:limit]

    async def get_book_details(self, external_id: str) -> Optional[BookDetails]:
        for client in self.clients:
            try:
                details = await client.get_book_details(external_id)
                if details:
                    return details
            except Exception:
                continue
        return None

    async def find_best_match(self, title: str, author: str) -> Optional[BookDetails]:
        for client in self.clients:
            try:
                details = await client.find_best_match(title, author)
                if details:
                    return details
            except Exception:
                continue
        return None

    def _deduplicate_results(self, results: List[BookSearchResult]) -> List[BookSearchResult]:
        seen = set()
        unique_results = []
        for result in results:
            key = (result.title.lower(), result.author.lower())
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        return unique_results