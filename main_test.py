from utils.EmailService import EmailService
from datetime import datetime
from logging_setup import setup_logging

setup_logging()
email_service = EmailService()

email_service.send_email(
    pdf_path="Academic Transcript.pdf",
    voucher_total=100.0,
    date=datetime.now()
)
