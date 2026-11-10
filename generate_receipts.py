import os
from fpdf import FPDF
from my_cloudinary import upload_pdf


def create_pdf(payment_data, trans_code):
    os.makedirs("receipts", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, str(payment_data), align="C")

    file_path = f"receipts/{trans_code}.pdf"
    pdf.output(file_path)

    receipt_url = upload_pdf(file_path)

    print("PDF receipt created successfully!")
    print("receipt link:", receipt_url)

    return receipt_url


# Test the PDF receipt
if __name__ == "__main__":
    create_pdf(
        "Transaction code: TEST123, Amount: 100 KES",
        "TEST123"
    )

