from datetime import datetime
from models.user import UserDb
from db.database import Base
from models.base import *

class InvoiceDb(Base):
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserDb"] = relationship("UserDb", back_populates="invoices")
