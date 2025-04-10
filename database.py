from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) # type: ignore

async def get_db():
    async with async_session_maker() as session:
        yield session

async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)