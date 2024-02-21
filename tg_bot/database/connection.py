from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, session

from tg_bot.data.config import url

async_engine = create_async_engine(url=url, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

