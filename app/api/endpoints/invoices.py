import asyncio
from datetime import datetime
from typing import Annotated

from db.user_db import init_default_user
from db.database import get_db
from auth.dependencies import get_current_active_user, verify_token
from auth.models import User
from fastapi import Form, Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
from starlette.templating import _TemplateResponse
from models.invoice_fields import InvoiceFields
from services.number_to_word import number_to_word  # Correct import
from services.invoice_calculator import InvoiceCounter
from services.pdf_creator import PdfCreator
from db.invoices_db import create_invoice, get_latest_invoice

from fastapi import APIRouter, Request
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

templates_dir = project_root / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


invoice_dict_global = None


@router.get("/")
async def send_invoice_webpage(
    request: Request, current_user: User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)
) -> _TemplateResponse:
    latest_invoice = await get_latest_invoice(db)
    await init_default_user(db)
    return templates.TemplateResponse(
        request=request,
        name="invoice_form.jinja",
        context={"latest_invoice": latest_invoice, "invoice_fields": InvoiceFields},
    )


@router.get("/invoice")
async def send_invoice_webpage(
    request: Request, current_user: User = Depends(get_current_active_user)
) -> _TemplateResponse:
    invoice_number = request.query_params.get("invoice_number")
    invoice_date = request.query_params.get("invoice_date")
    invoice_pay_date = request.query_params.get("invoice_pay_date")
    invoice_pay_type = request.query_params.get("invoice_pay_type")
    invoice_account_number = request.query_params.get("invoice_account_number")
    invoice_seller_name = request.query_params.get("invoice_seller_name")
    invoice_seller_address = request.query_params.get("invoice_seller_address")
    invoice_seller_nip = request.query_params.get("invoice_seller_nip")
    invoice_buyer_name = request.query_params.get("invoice_buyer_name")
    invoice_buyer_address = request.query_params.get("invoice_buyer_address")
    invoice_buyer_nip = request.query_params.get("invoice_buyer_nip")
    invoice_specification = request.query_params.get("invoice_specification")
    invoice_classification = request.query_params.get("invoice_classification")
    invoice_unit_measure = request.query_params.get("invoice_unit_measure")
    invoice_hour_rates = request.query_params.get("invoice_hour_rates")
    invoice_hours_number = request.query_params.get("invoice_hours_number")
    invoice_signature_left = request.query_params.get("invoice_signature_left")
    invoice_signature_right = request.query_params.get("invoice_signature_right")

    invoice_counter = InvoiceCounter(invoice_hour_rates, invoice_hours_number)
    invoice_dict = {
        "invoice_top_section": {
            "invoice_number": (invoice_number, InvoiceFields.invoice_number.value),
            "invoice_date": (invoice_date, InvoiceFields.invoice_date.value),
            "invoice_pay_date": (
                invoice_pay_date,
                InvoiceFields.invoice_pay_date.value,
            ),
            "invoice_pay_type": (
                invoice_pay_type,
                InvoiceFields.invoice_pay_type.value,
            ),
            "invoice_account_number": (
                invoice_account_number,
                InvoiceFields.invoice_account_number.value,
            ),
        },
        "invoice_middle_section": {
            "invoice_seller_name": (
                invoice_seller_name,
                InvoiceFields.invoice_seller_name.value,
            ),
            "invoice_seller_address": (
                invoice_seller_address,
                InvoiceFields.invoice_seller_address.value,
            ),
            "invoice_seller_nip": (
                invoice_seller_nip,
                InvoiceFields.invoice_seller_nip.value,
            ),
            "invoice_buyer_name": (
                invoice_buyer_name,
                InvoiceFields.invoice_buyer_name.value,
            ),
            "invoice_buyer_address": (
                invoice_buyer_address,
                InvoiceFields.invoice_buyer_address.value,
            ),
            "invoice_buyer_nip": (
                invoice_buyer_nip,
                InvoiceFields.invoice_buyer_nip.value,
            ),
        },
        "invoice_horizontal_section": {
            "invoice_specification": (
                invoice_specification,
                InvoiceFields.invoice_specification.value,
                "specification",
            ),
            "invoice_classification": (
                invoice_classification,
                InvoiceFields.invoice_classification.value,
                "classification",
            ),
            "invoice_unit_measure": (
                invoice_unit_measure,
                InvoiceFields.invoice_unit_measure.value,
                "unit-measure",
            ),
            "invoice_hour_rates": (
                invoice_hour_rates,
                InvoiceFields.invoice_hour_rates.value,
                "horizontal__hour-rates",
            ),
            "invoice_hours_number": (
                invoice_hours_number,
                InvoiceFields.invoice_hours_number.value,
                "hours-number",
            ),
        },
        "invoice_bottom_section": {
            "invoice_netto_value": (
                invoice_counter.get_netto_value(),
                InvoiceFields.invoice_netto_value.value,
            ),
            "invoice_vat_value": (
                invoice_counter.get_vat_value(),
                InvoiceFields.invoice_vat_value.value,
            ),
            "invoice_brutto_value": (
                invoice_counter.get_brutto_value(),
                InvoiceFields.invoice_brutto_value.value,
            ),
            "invoice_currency": (
                "PLN",
                InvoiceFields.invoice_currency.value,
            ),
            "invoice_value_in_words": (
                number_to_word(float(invoice_counter.get_brutto_value())),
                InvoiceFields.invoice_value_in_words.value,
            ),
        },
        "invoice_signature_left": invoice_signature_left,
        "invoice_signature_right": invoice_signature_right,
    }

    return templates.TemplateResponse(
        request=request,
        name="invoice_page.jinja",
        context={"invoice_dict": invoice_dict, "invoice_fields": InvoiceFields},
    )


@router.get("/invoice-pdf")
async def send_invoice_webpage(request: Request) -> _TemplateResponse:
    global invoice_dict_global
    invoice_number = request.query_params.get("invoice_number")
    invoice_date = request.query_params.get("invoice_date")
    invoice_pay_date = request.query_params.get("invoice_pay_date")
    invoice_pay_type = request.query_params.get("invoice_pay_type")
    invoice_account_number = request.query_params.get("invoice_account_number")
    invoice_seller_name = request.query_params.get("invoice_seller_name")
    invoice_seller_address = request.query_params.get("invoice_seller_address")
    invoice_seller_nip = request.query_params.get("invoice_seller_nip")
    invoice_buyer_name = request.query_params.get("invoice_buyer_name")
    invoice_buyer_address = request.query_params.get("invoice_buyer_address")
    invoice_buyer_nip = request.query_params.get("invoice_buyer_nip")
    invoice_specification = request.query_params.get("invoice_specification")
    invoice_classification = request.query_params.get("invoice_classification")
    invoice_unit_measure = request.query_params.get("invoice_unit_measure")
    invoice_hour_rates = request.query_params.get("invoice_hour_rates")
    invoice_hours_number = request.query_params.get("invoice_hours_number")
    invoice_signature_left = request.query_params.get("invoice_signature_left")
    invoice_signature_right = request.query_params.get("invoice_signature_right")

    invoice_counter = InvoiceCounter(invoice_hour_rates, invoice_hours_number)
    invoice_dict_global = {
        "invoice_number": (invoice_number, InvoiceFields.invoice_number.value),
        "invoice_date": (invoice_date, InvoiceFields.invoice_date.value),
        "invoice_pay_date": (invoice_pay_date, InvoiceFields.invoice_pay_date.value),
        "invoice_pay_type": (invoice_pay_type, InvoiceFields.invoice_pay_type.value),
        "invoice_account_number": (
            invoice_account_number,
            InvoiceFields.invoice_account_number.value,
        ),
        "invoice_seller_name": (
            invoice_seller_name,
            InvoiceFields.invoice_seller_name.value,
        ),
        "invoice_seller_address": (
            invoice_seller_address,
            InvoiceFields.invoice_seller_address.value,
        ),
        "invoice_seller_nip": (
            invoice_seller_nip,
            InvoiceFields.invoice_seller_nip.value,
        ),
        "invoice_buyer_name": (
            invoice_buyer_name,
            InvoiceFields.invoice_buyer_name.value,
        ),
        "invoice_buyer_address": (
            invoice_buyer_address,
            InvoiceFields.invoice_buyer_address.value,
        ),
        "invoice_buyer_nip": (
            invoice_buyer_nip,
            InvoiceFields.invoice_buyer_nip.value,
        ),
        "invoice_specification": (
            invoice_specification,
            InvoiceFields.invoice_specification.value,
        ),
        "invoice_classification": (
            invoice_classification,
            InvoiceFields.invoice_classification.value,
        ),
        "invoice_unit_measure": (
            invoice_unit_measure,
            InvoiceFields.invoice_unit_measure.value,
        ),
        "invoice_hour_rates": (
            invoice_hour_rates,
            InvoiceFields.invoice_hour_rates.value,
        ),
        "invoice_hours_number": (
            invoice_hours_number,
            InvoiceFields.invoice_hours_number.value,
        ),
        "invoice_netto_value": (
            invoice_counter.get_netto_value(),
            InvoiceFields.invoice_netto_value.value,
        ),
        "invoice_vat_value": (
            invoice_counter.get_vat_value(),
            InvoiceFields.invoice_vat_value.value,
        ),
        "invoice_brutto_value": (
            invoice_counter.get_brutto_value(),
            InvoiceFields.invoice_brutto_value.value,
        ),
        "invoice_currency": (
            "PLN",
            InvoiceFields.invoice_currency.value,
        ),
        "invoice_value_in_words": (
            (
                number_to_word(float(invoice_counter.get_brutto_value())),
                InvoiceFields.invoice_value_in_words.value,
            )
        ),
        "invoice_signature_left": (invoice_signature_left),
        "invoice_signature_right": (invoice_signature_right),
    }

    return templates.TemplateResponse(
        request=request, name="invoice_pdf.jinja", context=invoice_dict_global
    )


@router.get("/file")
def send_file(request: Request) -> FileResponse:
    invoice_file_path = "./output3.pdf"
    custom_filename = "output3.pdf"

    return FileResponse(invoice_file_path, status_code=200, filename=custom_filename)


@router.post("/form", status_code=201)
async def get_form(
    request: Request,
    invoice_number: Annotated[str, Form()],
    invoice_date: Annotated[str, Form()],
    invoice_pay_date: Annotated[str, Form()],
    invoice_pay_type: Annotated[str, Form()],
    invoice_account_number: Annotated[str, Form()],
    invoice_seller_name: Annotated[str, Form()],
    invoice_seller_address: Annotated[str, Form()],
    invoice_seller_nip: Annotated[str, Form()],
    invoice_buyer_name: Annotated[str, Form()],
    invoice_buyer_address: Annotated[str, Form()],
    invoice_buyer_nip: Annotated[str, Form()],
    invoice_specification: Annotated[str, Form()],
    invoice_classification: Annotated[str, Form()],
    invoice_unit_measure: Annotated[str, Form()],
    invoice_hour_rates: Annotated[str, Form()],
    invoice_hours_number: Annotated[str, Form()],
    invoice_signature_left: Annotated[str, Form()],
    invoice_signature_right: Annotated[str, Form()],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),  # Add db session
) -> RedirectResponse:

    invoice_dict = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "invoice_pay_date": invoice_pay_date,
        "invoice_pay_type": invoice_pay_type,
        "invoice_account_number": invoice_account_number,
        "invoice_seller_name": invoice_seller_name,
        "invoice_seller_address": invoice_seller_address,
        "invoice_seller_nip": invoice_seller_nip,
        "invoice_buyer_name": invoice_buyer_name,
        "invoice_buyer_address": invoice_buyer_address,
        "invoice_buyer_nip": invoice_buyer_nip,
        "invoice_specification": invoice_specification,
        "invoice_classification": invoice_classification,
        "invoice_unit_measure": invoice_unit_measure,
        "invoice_unit_measure": invoice_unit_measure,
        "invoice_unit_measure": invoice_unit_measure,
        "invoice_hour_rates": invoice_hour_rates,
        "invoice_hours_number": invoice_hours_number,
        "invoice_signature_left": invoice_signature_left,
        "invoice_signature_right": invoice_signature_right,
    }

    redirect_url = "/invoice?" + "&".join(
        f"{key}={value}"
        for key, value in {
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "invoice_pay_date": invoice_pay_date,
            "invoice_pay_type": invoice_pay_type,
            "invoice_account_number": invoice_account_number,
            "invoice_seller_name": invoice_seller_name,
            "invoice_seller_address": invoice_seller_address,
            "invoice_seller_nip": invoice_seller_nip,
            "invoice_buyer_name": invoice_buyer_name,
            "invoice_buyer_address": invoice_buyer_address,
            "invoice_buyer_nip": invoice_buyer_nip,
            "invoice_specification": invoice_specification,
            "invoice_classification": invoice_classification,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_hour_rates": invoice_hour_rates,
            "invoice_hours_number": invoice_hours_number,
            "invoice_signature_left": invoice_signature_left,
            "invoice_signature_right": invoice_signature_right,
        }.items()
    )

    url_pdf = "invoice-pdf?" + "&".join(
        f"{key}={value}"
        for key, value in {
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "invoice_pay_date": invoice_pay_date,
            "invoice_pay_type": invoice_pay_type,
            "invoice_account_number": invoice_account_number,
            "invoice_seller_name": invoice_seller_name,
            "invoice_seller_address": invoice_seller_address,
            "invoice_seller_nip": invoice_seller_nip,
            "invoice_buyer_name": invoice_buyer_name,
            "invoice_buyer_address": invoice_buyer_address,
            "invoice_buyer_nip": invoice_buyer_nip,
            "invoice_specification": invoice_specification,
            "invoice_classification": invoice_classification,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_unit_measure": invoice_unit_measure,
            "invoice_hour_rates": invoice_hour_rates,
            "invoice_hours_number": invoice_hours_number,
            "invoice_signature_left": invoice_signature_left,
            "invoice_signature_right": invoice_signature_right,
        }.items()
    )

    try:
        pdf_creator = PdfCreator(str(request.base_url) + url_pdf)
        await asyncio.gather(
            pdf_creator.create_pdf_async(),
            create_invoice(invoice_data=invoice_dict, db=db),
        )
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        # Handle the error appropriately

    response = RedirectResponse(url=redirect_url, status_code=301)

    return response
