import pdfplumber
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


pdf = pdfplumber.open("oligopoly chapter AQA.pdf")

text = ""

for i, page in enumerate(pdf.pages, start=1):
    print(f"OCR on page {i}...")
    img = page.to_image(resolution=300).original
    page_text = pytesseract.image_to_string(img)
    text += page_text

print(text[:500])
