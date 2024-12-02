import pdfkit


class PdfCreator:
    # Configure PDF options
    options = {
        "page-size": "A4",
        "margin-top": "10mm",
        "margin-right": "20mm",
        "margin-bottom": "10mm",
        "margin-left": "20mm",
    }

    output_pdf_path = "output3.pdf"

    def __init__(self, website_url) -> None:
        self.website_url = website_url

    def create_pdf(self):
        print(f"Creating PDF from {self.website_url}")
        pdfkit.from_url(self.website_url, self.output_pdf_path, options=self.options)

if __name__ == "__main__":
    pdf_creator = PdfCreator("http://0.0.0.0:8000/")
    pdf_creator.create_pdf()