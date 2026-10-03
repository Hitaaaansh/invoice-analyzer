import cv2
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread("receiptimage.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

data = pytesseract.image_to_data(gray, output_type=Output.DICT)

words = []

for i in range(len(data["text"])):
    text = data["text"][i].strip()

    if text:
        words.append({
            "text": text,
            "x": data["left"][i],
            "y": data["top"][i],
            "w": data["width"][i],
            "h": data["height"][i]
        })

items = []
current_item = ""

for word in words:
    if 410 <= word["y"] <= 510 and word["x"] < 400:
        text = word["text"]

        if text.isdigit() and 1 <= int(text) <= 9:
            if current_item:
                items.append(current_item.strip())
            current_item = ""
        elif text != "|":
            current_item += text + " "

if current_item:
    items.append(current_item.strip())

prices = []
amounts = []

for word in words:
    text = word["text"].replace("$", "")

    if 410 <= word["y"] <= 510 and word["x"] >= 450:
        try:
            value = float(text)

            if word["x"] < 580:
                prices.append(value)
            else:
                amounts.append(value)

        except ValueError:
            pass

print("ITEMS:")

for i in range(len(items)):
    price = prices[i] if i < len(prices) else "Not found"
    amount = amounts[i] if i < len(amounts) else "Not found"

    print(f"{i + 1}. {items[i]}")
    print(f"   Unit Price: {price}")
    print(f"   Amount: {amount}")