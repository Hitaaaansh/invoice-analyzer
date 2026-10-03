import cv2
import pytesseract
from exctractor import extract_information, extract_invoice_items

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread("sample 2.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

text = pytesseract.image_to_string(gray)

result = extract_information(text)
items = extract_invoice_items(text)

print("EXTRACTED INFORMATION")
print("Merchant:", result["merchant"])
print("Date:", result["date"])
print("Total:", result["total"])

print("\nITEMS")

for item in items:
    print("Description:", item["description"])
    print("Quantity:", item["quantity"])
    print("Rate:", item["rate"])
    print("Amount:", item["amount"])