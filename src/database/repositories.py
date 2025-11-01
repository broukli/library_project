from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ..use_case.entities import Book
from ..repository.books_repository import BookRepository
from .models import BookModel
from .settings import settings


class PostgreSQLBookRepository(BookRepository):
    """Реализация репозитория для PostgreSQL"""

    def __init__(self):
        self.engine = create_engine(
            settings.database.database_url,
            echo=settings.database.echo_sql
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._init_database()

    def _init_database(self):
        """Инициализация базы данных"""
        BookModel.metadata.create_all(bind=self.engine)

    def _to_entity(self, model: BookModel) -> Book:
        """Преобразование модели в сущность"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            year=model.year,
            genre=model.genre,
            pages=model.pages,
            is_available=model.is_available,
            cover_url=model.cover_url,
            description=model.description,
            rating=model.rating,
            isbn=model.isbn,
            publisher=model.publisher,
            language=model.language,
        )

    def _to_model(self, entity: Book) -> BookModel:
        """Преобразование сущности в модель"""
        return BookModel(
            id=entity.id,
            title=entity.title,
            author=entity.author,
            year=entity.year,
            genre=entity.genre,
            pages=entity.pages,
            is_available=entity.is_available,
            cover_url=entity.cover_url,
            description=entity.description,
            rating=entity.rating,
            isbn=entity.isbn,
            publisher=entity.publisher,
            language=entity.language
        )

    async def get_all(self) -> List[Book]:
        db = self.SessionLocal()
        try:
            books = db.query(BookModel).order_by(BookModel.id).all()
            return [self._to_entity(book) for book in books]
        finally:
            db.close()

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        db = self.SessionLocal()
        try:
            book = db.query(BookModel).filter(BookModel.id == book_id).first()
            return self._to_entity(book) if book else None
        finally:
            db.close()

    async def create(self, book: Book) -> Book:
        db = self.SessionLocal()
        try:
            db_book = self._to_model(book)
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return self._to_entity(db_book)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    async def update(self, book_id: int, book: Book) -> Optional[Book]:
        db = self.SessionLocal()
        try:
            db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
            if not db_book:
                return None

            # Обновляем поля
            for field, value in book.model_dump(exclude={'id'}).items():
                setattr(db_book, field, value)

            db.commit()
            db.refresh(db_book)
            return self._to_entity(db_book)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    async def delete(self, book_id: int) -> bool:
        db = self.SessionLocal()
        try:
            db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
            if not db_book:
                return False

            db.delete(db_book)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    async def search(self, query: str) -> List[Book]:
        db = self.SessionLocal()
        try:
            books = db.query(BookModel).filter(
                (BookModel.title.ilike(f"%{query}%")) |
                (BookModel.author.ilike(f"%{query}%"))
            ).all()
            return [self._to_entity(book) for book in books]
        finally:
            db.close()