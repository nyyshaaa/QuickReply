from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from backend.config.settings import config_settings

DATABASE_URL = config_settings.DATABASE_URL

async_engine=create_async_engine(DATABASE_URL,echo=False)

async_session=async_sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)