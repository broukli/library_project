from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""
    database_url: str = "postgresql+psycopg2://postgres:password@localhost:5432/book_library"
    echo_sql: bool = False

    class Config:
        env_prefix = "DB_"


class ApiSettings(BaseSettings):
    """Настройки внешних API"""
    open_library_base_url: str = "https://openlibrary.org"
    request_timeout: float = 30.0

    class Config:
        env_prefix = "API_"


class Settings(BaseSettings):
    """Общие настройки приложения"""
    database: DatabaseSettings = DatabaseSettings()
    api: ApiSettings = ApiSettings()
    app_name: str = "Book Library API"
    debug: bool = False


settings = Settings()