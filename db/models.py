from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime

from datetime import datetime

class Base(DeclarativeBase):
    pass 


class Clients(Base):
    __tablename__ = 'clients'

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    is_ban: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None) 

class Cars(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    license_plate: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("drivers.telegram_id"))

    owner: Mapped["Drivers"] = relationship(back_populates="cars")




class Drivers(Base):
    __tablename__ = 'drivers'

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    is_ban: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)

    cars: Mapped[List["Cars"]] = relationship(back_populates="owner")
