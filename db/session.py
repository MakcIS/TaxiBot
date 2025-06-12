from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from db.models import Base
from config_data import settings

db_conf = settings.get_settings().db_config

DB_URL = f"postgresql+asyncpg://{db_conf.user}:{db_conf.password}@db:{db_conf.port}/{db_conf.database}"

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)