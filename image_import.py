from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
def extract_text(path):

    img = Image.open(path)

    text = pytesseract.image_to_string(
        img,
        lang="eng + hin"
    )

    return text