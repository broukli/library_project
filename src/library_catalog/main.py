from fastapi import FastAPI
from ..routers.routers import router as books_router
from ..database.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Подключаем роутеры
app.include_router(books_router)

