import cv2
import pytesseract
import streamlit as st
import tempfile
import os
from exctractor import extract_information, extract_invoice_items


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


st.set_page_config(
    page_title="Receipt & Invoice Analyzer",
    page_icon="🧾",
    layout="wide"
)


st.title("🧾 Receipt & Invoice Analyzer")
st.write(
    "Upload a receipt or invoice to automatically extract "
    "important information and item details."
)

st.divider()


uploaded_file = st.file_uploader(
    "Upload your document",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file:

    file_extension = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp:

        temp.write(uploaded_file.read())
        image_path = temp.name

    image = cv2.imread(image_path)

    with st.spinner("Processing document..."):

        # Image preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # OCR
        text = pytesseract.image_to_string(gray)

        # Information extraction
        result = extract_information(text)
        items = extract_invoice_items(text)

    st.success("Document processed successfully!")

    st.divider()

    # -----------------------------
    # Document Preview
    # -----------------------------

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("Document Preview")

        st.image(
            image,
            use_container_width=True
        )

    # -----------------------------
    # Extracted Information
    # -----------------------------

    with col2:

        st.subheader("Extracted Information")

        st.metric(
            "Merchant",
            result["merchant"]
        )

        st.metric(
            "Date",
            result["date"]
        )

        st.metric(
            "Total Amount",
            result["total"]
        )

    st.divider()

    # -----------------------------
    # Items
    # -----------------------------

    st.subheader("Extracted Items")

    if items:

        table_data = []

        for item in items:

            table_data.append({
                "Description": item["description"],
                "Quantity": item["quantity"],
                "Unit Price": item["rate"],
                "Amount": item["amount"]
            })

        st.table(table_data)

    else:

        st.info("No item details could be extracted.")

    # -----------------------------
    # Raw OCR
    # -----------------------------

    with st.expander("View Raw OCR Text"):

        st.text(text)

    # Remove temporary file
    os.remove(image_path)