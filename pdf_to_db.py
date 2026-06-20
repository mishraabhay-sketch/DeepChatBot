from pdf_import import extract_text
from database import add_pdf_data

def import_pdf(pdf_path):

    text = extract_text(pdf_path)

    if not text:
        return

    paragraphs = text.split("\n")

    for para in paragraphs:

        para = para.strip()

        if len(para) > 20:

            add_pdf_data(
                para[:100],
                para
            )

    print("PDF Imported Successfully")