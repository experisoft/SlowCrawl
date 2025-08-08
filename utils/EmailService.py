import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

class EmailService:
    """EmailService class to handle sending emails with an attached PDF voucher report."""
    
    def __init__(self):
        # Store SMTP configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.username = os.getenv('SENDER_EMAIL_USERNAME')
        self.password = os.getenv('SENDER_EMAIL_PASSWORD')
        self.receiver_email = os.getenv('RECEIVER_EMAIL')
        
        # Validate that all required credentials are available
        if not all([self.smtp_server, self.smtp_port, self.username, self.password]):
            logger.error("Missing SMTP credentials. Please check your .env file.")
            raise ValueError("Missing SMTP credentials. Please check your .env file or provide parameters.")

    def _compose_voucher_email(self, voucher_total: float, date: datetime, pdf_path: str):
        """
        Compose the email message with PDF attachment for voucher report.
        
        Args:
            voucher_total: The total value of vouchers
            date: The date for the report
            pdf_path: Path to the PDF file to attach
            
        Returns:
            MIMEMultipart: Composed email message
        """
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.receiver_email
        msg['Subject'] = f"Voucher Report - {date.strftime('%Y-%m-%d')} - Total: £{voucher_total:.2f}"
        
        # Create email body
        body = f"Attached is the voucher report for {date.strftime('%Y-%m-%d')}.\nTotal Voucher Value: £{voucher_total:.2f}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF file
        try:
            with open(pdf_path, 'rb') as f:
                msg.attach(MIMEApplication(f.read(), 'pdf', name=pdf_path))
            logger.debug(f"PDF attachment added successfully: {pdf_path}")
        except FileNotFoundError:
            logger.error(f"PDF file not found: {pdf_path}")
            raise
        except Exception as e:
            logger.error(f"Error attaching PDF file: {e}")
            raise
        return msg

    def send_email(self, pdf_path: str, voucher_total: float, date: datetime):
        """
        Send an email with the voucher report PDF attached.
        
        Args:
            pdf_path: Path to the PDF file to attach
            voucher_total: The total monetary value of vouchers
            date: The date of report generation
        """
        
        client = smtplib.SMTP(self.smtp_server, self.smtp_port)
        try:
            logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            client.starttls()
            client.login(self.username, self.password)
            logger.info("SMTP connection established and authentication successful")
            
            # Compose the email message
            msg = self._compose_voucher_email(voucher_total, date, pdf_path)
            logger.debug(f"Email composed for recipient: {self.receiver_email}")

            client.send_message(msg)
            logger.info(f"Email sent successfully to {self.receiver_email} - Voucher report for {date.strftime('%Y-%m-%d')} (Total: £{voucher_total:.2f})")
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check your username/password.")
            raise
        except smtplib.SMTPConnectError:
            logger.error(f"Failed to connect to SMTP server: {self.smtp_server}:{self.smtp_port}")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while sending email: {e}")
            raise
        finally:
            client.quit()
            logger.info("SMTP connection closed")
