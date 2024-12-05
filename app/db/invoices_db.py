from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional
from db.database import get_db
from models.invoice import Invoice
from datetime import datetime


def convert_date_string(date_str: str) -> datetime.date:
    """Convert string date to Python date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


async def create_invoice(invoice_data: Dict[str, Any], db: AsyncSession) -> Invoice:
    """Create a new invoice using SQLAlchemy async ORM"""
    try:

        # Convert date strings to date objects
        invoice_data["invoice_date"] = convert_date_string(invoice_data["invoice_date"])
        invoice_data["invoice_pay_date"] = convert_date_string(
            invoice_data["invoice_pay_date"]
        )
        # Create new Invoice instance
        invoice = Invoice(
            invoice_number=invoice_data["invoice_number"],
            invoice_date=invoice_data["invoice_date"],
            invoice_pay_date=invoice_data["invoice_pay_date"],
            invoice_pay_type=invoice_data["invoice_pay_type"],
            invoice_account_number=invoice_data["invoice_account_number"],
            invoice_seller_name=invoice_data["invoice_seller_name"],
            invoice_seller_address=invoice_data["invoice_seller_address"],
            invoice_seller_nip=invoice_data["invoice_seller_nip"],
            invoice_buyer_name=invoice_data["invoice_buyer_name"],
            invoice_buyer_address=invoice_data["invoice_buyer_address"],
            invoice_buyer_nip=invoice_data["invoice_buyer_nip"],
            invoice_specification=invoice_data["invoice_specification"],
            invoice_classification=invoice_data["invoice_classification"],
            invoice_unit_measure=invoice_data["invoice_unit_measure"],
            invoice_hour_rates=invoice_data["invoice_hour_rates"],
            invoice_hours_number=invoice_data["invoice_hours_number"],
            invoice_signature_left=invoice_data["invoice_signature_left"],
            invoice_signature_right=invoice_data["invoice_signature_right"],
        )

        db.add(invoice)
        await db.commit()
        return invoice

    except Exception as e:
        await db.rollback()
        raise ValueError(f"Failed to create invoice: {str(e)}")


async def get_latest_invoice(db: AsyncSession) -> Optional[Invoice]:
    """Get the latest invoice using SQLAlchemy async ORM"""
    try:
        print("KOZAAAA")
        # Create query to get latest invoice
        query = select(Invoice).order_by(Invoice.id.desc()).limit(1)

        # Execute query
        result = await db.execute(query)
        print("result", result)
        invoice = result.scalar_one_or_none()
        print("invoice LATEST", invoice)

        return invoice

    except Exception as e:
        print("An error occurred:", e)
