from sqlalchemy import Column, Integer, String, Boolean, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BookModel(Base):
    """SQLAlchemy модель книги"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=False)
    pages = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

    # Дополнительная информация
    cover_url = Column(Text)
    description = Column(Text)
    rating = Column(Float)
    isbn = Column(String(20))
    publisher = Column(String(255))
    language = Column(String(10), default='en')
