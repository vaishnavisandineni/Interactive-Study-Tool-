# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)

# --- SET TESSERACT PATH ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------- OCR FUNCTION ----------
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                print(f"OCR on page {page_number}...")
                # convert page to image
                img = page.to_image(resolution=300).original
                # extract OCR text
                page_text = pytesseract.image_to_string(img)
                text += page_text + "\n"
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return ""
    return text

# -------- LOAD PDF AT STARTUP ----------
PDF_PATH = r"C:\Users\vaish\interactive-study-tool\backend\oligopoly chapter AQA.pdf"
print("Extracting text from PDF using OCR...")
chapter_text = extract_text_from_pdf(PDF_PATH)
if chapter_text:
    print("OCR extraction complete!")
else:
    print("OCR extraction failed. Check the PDF path!")

# -------- ROUTES ----------
@app.route("/")
def home():
    return "Backend is running. Use /chapter or /ask."

@app.route("/chapter", methods=["GET"])
def get_chapter():
    return jsonify({"text": chapter_text})

@app.route("/ask", methods=["POST"])
def ask():
    if not request.is_json:
        return jsonify({"answer": "Error: Content-Type must be application/json"}), 415

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please ask a question."})

    # Dummy answer: return question + first part of PDF
    answer = f"You asked: {question}\n\nHere is part of the chapter:\n{chapter_text[:700]}..."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
