from fastapi import FastAPI

from src.presentation.errors_handlers.error_handlers import error_handlers
from src.presentation.routes import router as main_router

app = FastAPI()

app.include_router(main_router)
error_handlers(app)
