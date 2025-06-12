from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime

from datetime import datetime

class Base(DeclarativeBase):
    pass 


class Clients(Base):
    __tablename__ = 'clients'

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    is_ban: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None) 

