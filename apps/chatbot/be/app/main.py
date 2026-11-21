import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.concurrency import run_in_threadpool

from .config import Settings
from .routes import router
from .store import Store


def create_app(settings: Settings | None = None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        app.state.store = await run_in_threadpool(Store, settings)
        yield
        await run_in_threadpool(app.state.store.engine.dispose)

    app = FastAPI(title="Weconomy Chat API", lifespan=lifespan)
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        logging.error("Chat database operation failed (%s)", type(exc).__name__)
        return JSONResponse({"detail": "Chat database unavailable"}, status_code=503)

    app.include_router(router)

    return app


app = create_app()
