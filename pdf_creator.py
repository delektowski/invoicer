import pdfkit


class PdfCreator:
    # Configure PDF options
    options = {
        "page-size": "A4",
        "margin-top": "20mm",
        "margin-right": "20mm",
        "margin-bottom": "20mm",
        "margin-left": "20mm",
    }

    output_pdf_path = "output3.pdf"

    def __init__(self, website_url) -> None:
        print('fik', website_url)
        self.website_url = website_url

    def create_pdf(self):
        print("pipipi")
        pdfkit.from_url(self.website_url, self.output_pdf_path, options=self.options)

if __name__ == "__main__":
    pdf_creator = PdfCreator("http://127.0.0.1:8000")
    pdf_creator.create_pdf()