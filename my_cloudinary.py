import cloudinary
import cloudinary.uploader
import os
from send_email import email


Cloud_Name = "nofybpkz"
Api_Key = "375199336376633"
Secret_Key = "CB19bpE6NRspmt2wAcV1h594pkA"

# connecting to cloudinary
cloudinary.config(
    cloud_name=Cloud_Name,
    api_key=Api_Key,
    api_secret=Secret_Key
)

print("Cloudinary configuration successful")



def upload_pdf(file_path):
    try:
        # 1. Check if the file exists at the given path
        if not os.path.exists(file_path):
            print(f"Upload failed: File not found at {file_path}")
            return "failed"

        # 2. Upload the file directly to Cloudinary using its exact path
        upload = cloudinary.uploader.upload(
            file_path,
            resource_type="auto"
        )

        receipt_url = upload["secure_url"]

        print("Cloudinary receipt URL:", receipt_url)
        print("PDF uploaded successfully")

        #send email
        email("aabdimalik09@gmail.com","payment received",f"thank you we have received your payments.\n\n" f"receipts: {receipt_url}")
        return receipt_url

    except Exception as e:
        print(f"Upload failed: {e}")
        return "failed"