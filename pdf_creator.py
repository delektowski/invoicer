import pdfkit


class PdfCreator:
    # Configure PDF options
    options = {
        "page-size": "A4",
        "margin-top": "0mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
    }

    output_pdf_path = "output2.pdf"

    def __init__(self, website_url) -> None:
        self.website_url = website_url

    def create_pdf(self):
        pdfkit.from_url(self.website_url, self.output_pdf_path, options=self.options)
