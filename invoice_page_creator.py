from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from count_invoice import InvoiceCounter
from number_to_word import number_to_word


class InvoicePageCreator(InvoiceCounter):
    doc = Document("invoice_template.docx")
    properties_excluded_align_center = ["invoice_number", "invoice_date", "invoice_pay_date"]

    def __init__(
        self,
        invoice_number,
        invoice_date,
        invoice_pay_date,
        invoice_hour_rate,
        invoice_hours_number,
    ) -> None:
        super().__init__(invoice_hour_rate, invoice_hours_number)

        # Set fields values
        self.invoice_number_data = invoice_number
        self.invoice_date_data = invoice_date
        self.invoice_pay_date_data = invoice_pay_date
        self.invoice_hour_rate_data = invoice_hour_rate
        self.invoice_hours_number_data = invoice_hours_number

        # Set fields references in docx
        self.invoice_number = ""
        self.invoice_date = ""
        self.invoice_pay_date = ""
        self.invoice_hour_rate = ""
        self.invoice_hours_number = ""
        self.invoice_netto_value = ""
        self.invoice_vat_value = ""
        self.invoice_brutto_value = ""
        self.invoice_number_word = ""

    def write_invoice_fields(self):
        self.invoice_number.text = self.invoice_number_data
        self.invoice_date.text = self.invoice_date_data
        self.invoice_pay_date.text = self.invoice_pay_date_data
        self.invoice_hour_rate.text = self.invoice_hour_rate_data
        self.invoice_hours_number.text = self.invoice_hours_number_data
        self.invoice_netto_value.text = self.get_netto_value()
        self.invoice_vat_value.text = self.get_vat_value()
        self.invoice_brutto_value.text = self.get_brutto_value()
        self.invoice_number_word.text = number_to_word(float(self.get_brutto_value()))
