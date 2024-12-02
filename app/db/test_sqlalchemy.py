from datetime import datetime
from db.database import Base
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    insert,
    select,
    bindparam,
    Date,
    Text
)
from core.config import settings
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped




class Invoice(Base):
    __tablename__ = "invoices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(Text, nullable=False)
    invoice_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    invoice_pay_date: Mapped[datetime] = mapped_column(Date)
    invoice_pay_type: Mapped[str] = mapped_column(Text)
    invoice_account_number: Mapped[str] = mapped_column(Text)
    invoice_seller_name: Mapped[str] = mapped_column(Text, nullable=False)
    invoice_seller_address: Mapped[str] = mapped_column(Text)
    invoice_seller_nip: Mapped[str] = mapped_column(Text)
    invoice_buyer_name: Mapped[str] = mapped_column(Text, nullable=False)
    invoice_buyer_address: Mapped[str] = mapped_column(Text)
    invoice_buyer_nip: Mapped[str] = mapped_column(Text)
    invoice_specification: Mapped[str] = mapped_column(Text)
    invoice_classification: Mapped[str] = mapped_column(Text)
    invoice_unit_measure: Mapped[str] = mapped_column(Text)
    invoice_hour_rates: Mapped[int] = mapped_column(Integer)
    invoice_hours_number: Mapped[int] = mapped_column(Integer)
    invoice_signature_left: Mapped[str] = mapped_column(Text)
    invoice_signature_right: Mapped[str] = mapped_column(Text)

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String)  

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    email_address: Mapped[str] = mapped_column(String, nullable=False)  

# Create engine and tables
engine = create_engine(settings.DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

stmt = select(User).where(User.fullname.like("%Cheeks%"))


with engine.connect() as conn:
    conn.execute(
        insert(User),
        [
            {"name": "koza", "fullname": "koza Cheeks"},
            {"name": "krowa", "fullname": "krowa Cheeks"},
        ],
    )
    for row in conn.execute(stmt):
        print(row)
    conn.commit()
