# Invoice Analyzer

A computer vision pipeline that reads invoice/receipt images and converts them
into structured data.

## How it works
Image → OpenCV preprocessing → Tesseract OCR → regex-based extraction → Streamlit UI

## Features
- Upload an invoice or receipt image through a Streamlit interface
- Image preprocessing with OpenCV
- Text extraction using Tesseract OCR
- Extracts merchant, date, total, and line items (description, quantity, rate, amount)
- Shows the raw OCR text next to the structured result for inspection

## Tech stack
Python, OpenCV, Tesseract OCR (pytesseract), Pillow, Streamlit

## Setup
1. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and note its install path
2. Install dependencies: `pip install -r requirements.txt`
3. If needed, set the Tesseract path in the code (on Windows:
   `C:\Program Files\Tesseract-OCR\tesseract.exe`)
4. Run: `streamlit run app.py`

## Limitations
- Rule-based extraction depends on invoice layout
- OCR accuracy drops on blurry or low-quality images
- Tested on a small number of layouts so far

## Roadmap
- [ ] Bulk upload
- [ ] Review step for
