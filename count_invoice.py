class InvoiceCounter:
    def __init__(self, hour_rate: str, hours_number: str) -> None:
        self.hour_rate = hour_rate
        self.hours_number = hours_number

    def get_netto_value(self) -> str:
        return "{:.2f}".format(float(self.hour_rate) * float(self.hours_number))

    def get_vat_value(self) -> str:
        vat = 0.23
        netto_value = float(self.get_netto_value())
        return "{:.2f}".format(netto_value * vat)

    def get_brutto_value(self) -> str:
        return "{:.2f}".format(float(self.get_netto_value()) + float(self.get_vat_value()))
