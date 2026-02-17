from datetime import datetime

from sqlalchemy import Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100), default="general")
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())