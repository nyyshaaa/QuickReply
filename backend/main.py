
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from backend.app.custom_exceptions import register_all_exceptions
from backend.db.connection import async_engine,async_session
from backend.api.__init__ import cur_version
from backend.api.routers import public_routers
from backend.app.logging import setup_logging

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    setup_logging()

    try:
        yield
    finally:
        await async_engine.dispose()

        
def create_app():
    app=FastAPI(
        title="Phyllonix",
        version=cur_version,
        lifespan=app_lifespan)
    
    app.include_router(public_routers)

    register_all_exceptions(app)

    return app
 
app=create_app()