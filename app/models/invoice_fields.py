from enum import Enum

class InvoiceFields(str, Enum):
    invoice_number = "Faktura"
    invoice_date = "Data wystawienia"
    invoice_pay_date = "Termin zapłaty"
    invoice_pay_type = "Sposób zapłaty"
    invoice_account_number = "Konto bankowe"
    invoice_seller_name = "Nazwa sprzedawcy"
    invoice_seller_address = "Adres sprzedawcy"
    invoice_seller_nip = "NIP sprzedawcy"
    invoice_buyer_name = "Nazwa nabywcy"
    invoice_buyer_address = "Adres nabywcy"
    invoice_buyer_nip = "NIP nabywcy"
    invoice_order_number = "lp."
    invoice_specification = "Określenie towaru / usługi"
    invoice_classification = "PKWiU"
    invoice_unit_measure = "jm."
    invoice_hour_rates = "Cena jedn."
    invoice_hours_number = "Wartość"
    invoice_netto_value = "Wartość netto"
    invoice_vat_value = "Kwota VAT (23%)"
    invoice_brutto_value = "Wartość z podatkiem VAT"
    invoice_currency = "Waluta"
    invoice_value_in_words = "Słownie"
    

