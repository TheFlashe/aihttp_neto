import atexit
import datetime
import os

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}" f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_async_engine(DSN)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}


class Desk(Base):
    __tablename__ = "desk_aio"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    header: MappedColumn[str] = mapped_column(String(50))
    description: MappedColumn[str] = mapped_column(String(150))
    create_descr_time: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner: MappedColumn[str] = mapped_column(String(20))

    @property
    def dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "time_create": self.create_descr_time.isoformat(),
            "owner": self.owner,
        }


async def init_orm():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
