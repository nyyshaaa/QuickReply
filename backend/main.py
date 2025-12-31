
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from backend.db.connection import async_engine,async_session
from backend.api.__init__ import cur_version
from backend.api.routers import public_routers


@asynccontextmanager
async def app_lifespan(app: FastAPI):

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

    return app
 
app=create_app()