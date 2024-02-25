from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated
from count_invoice import InvoiceCounter
from db.invoices_db import get_invoice, handle_table_creation, insert_invoice
from number_to_word import number_to_word
from pdf_creator import PdfCreator


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

handle_table_creation()

@app.get("/")
async def send_invoice_webpage(request: Request):
    latest_invoice = get_invoice()
    return templates.TemplateResponse(request=request, name="invoice_form.html", context=latest_invoice)

@app.get("/invoice")
async def send_invoice_webpage(request: Request):
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
    
    invoice_counter = InvoiceCounter(invoice_hour_rates,invoice_hours_number)
    print("KOKOKO", float(invoice_counter.get_brutto_value()))
    print("IOIOIOOI", number_to_word(float(invoice_counter.get_brutto_value())))
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
        "invoice_netto_value": invoice_counter.get_netto_value(),
        "invoice_vat_value": invoice_counter.get_vat_value(),
        "invoice_brutto_value": invoice_counter.get_brutto_value(),
        "invoice_value_in_words": number_to_word(float(invoice_counter.get_brutto_value())),
   
    }
 
    return templates.TemplateResponse(
        request=request,
        name="invoice_page.html",
        context=invoice_dict
       
    )

@app.get("/file")
def send_file(request: Request):
    invoice_file_path ="./output3.pdf"
    custom_filename = "output3.pdf"

  
    return FileResponse(invoice_file_path, status_code=200, filename=custom_filename)

@app.post("/form", status_code=201)
def get_form(request: Request,
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
):
    
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
    }.items()
    )

    insert_invoice(table_name="invoices", data=tuple(invoice_dict.values()))
    pdf_creator = PdfCreator(str(request.base_url))
    pdf_creator.create_pdf()
    
    response = RedirectResponse(url=redirect_url, status_code=301)

    return response
