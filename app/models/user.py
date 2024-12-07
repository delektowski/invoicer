from datetime import datetime
from typing import List
from db.database import Base
from models.base import *

class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
    invoices: Mapped[List["Invoice"]] = relationship("InvoiceDb", back_populates="user")
