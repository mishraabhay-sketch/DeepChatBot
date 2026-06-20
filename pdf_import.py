import PyPDF2

def extract_text(pdf_path):

    text = ""

    try:
        with open(pdf_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print("PDF Error:", e)

    return text