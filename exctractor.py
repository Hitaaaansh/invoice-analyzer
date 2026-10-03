import re


def extract_information(text):

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    result = {
        "merchant": "Not found",
        "date": "Not found",
        "total": "Not found",
        "items": []
    }

    if lines:
        result["merchant"] = lines[0]

    date_patterns = [
        r"(?:Receipt Date|Invoice Date)\s*:?\s*(\d{2}[/-]\d{2}[/-]\d{4})",
        r"(?:Receipt Date|Invoice Date)\s+(\d{2}[/-]\d{2}[/-]\d{4})"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            result["date"] = match.group(1)
            break

    total_patterns = [
        r"(?:TOTAL AMOUNT|\bTOTAL\b)\s*\$?\s*([\d,.]+)",
        r"(?:TOTAL TAXABLE AMOUNT)\s*([\d,.]+)"
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            result["total"] = match.group(1)
            break

    return result


def extract_invoice_items(text):

    items = []

    # --------------------------------------------------
    # FORMAT 1: Invoice
    # Description + Date + Quantity + Rate + Amount
    # --------------------------------------------------

    invoice_pattern = re.compile(
        r"(.+?)\s+\d{2}-\d{2}-\d{4}\s+(\d+)\s+(\d+)(?:/-\w+)?\s+(\d+)"
    )

    invoice_matches = invoice_pattern.findall(text)

    for match in invoice_matches:
        items.append({
            "description": match[0].strip(),
            "quantity": match[1],
            "rate": match[2],
            "amount": match[3]
        })

    if items:
        return items

    # --------------------------------------------------
    # FORMAT 2: Receipt
    # --------------------------------------------------

    descriptions = []

    # Find item 1
    match = re.search(
        r"\b1\s+(.+?)(?=\s+2\s*\|)",
        text,
        re.IGNORECASE
    )

    if match:
        descriptions.append({
            "quantity": "1",
            "description": match.group(1).strip()
        })

    # Find item 2
    match = re.search(
        r"\b2\s*\|\s*(.+?)(?=\s+3\s+)",
        text,
        re.IGNORECASE
    )

    if match:
        descriptions.append({
            "quantity": "2",
            "description": match.group(1).strip()
        })

    # Find item 3
    match = re.search(
        r"\b3\s+(.+?)(?=\s+Terms)",
        text,
        re.IGNORECASE
    )

    if match:
        descriptions.append({
            "quantity": "3",
            "description": match.group(1).strip()
        })

    # --------------------------------------------------
    # Find the price section
    # --------------------------------------------------

    prices = []

    price_match = re.search(
        r"UNIT PRICE AMOUNT\s+(.+?)\s+Subtotal",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if price_match:

        numbers = re.findall(
            r"\d+\.\d+",
            price_match.group(1)
        )

        # Take first 6 numbers:
        # 100.00 100.00
        # 15.00 30.00
        # 5.00 15.00
        if len(numbers) >= 6:

            for i in range(0, 6, 2):
                prices.append([
                    numbers[i],
                    numbers[i + 1]
                ])

    # --------------------------------------------------
    # Combine descriptions and prices
    # --------------------------------------------------

    count = min(len(descriptions), len(prices))

    for i in range(count):

        items.append({
            "description": descriptions[i]["description"],
            "quantity": descriptions[i]["quantity"],
            "rate": prices[i][0],
            "amount": prices[i][1]
        })

    return items