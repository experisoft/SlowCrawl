"""
Script to automate the registration of new email addresses
- This script uses Playwright to interact with a web page and register email addresses.
- It includes functions to call an API, get email addresses, and apply delays between requests.
- It automates the registration process for a range of email addresses.

You must define TARGET_DOMAIN and EMAIL_FARM_DOMAIN in .env
Note there is rate limiting in place, so please space out your requests.
If you have access to a VPN or proxy, you may want to use it to avoid rate limiting.
A rate over 10 new registrations per hour will result in temporary bans.
"""

import os
import time
import random
import dotenv
from playwright.sync_api import sync_playwright

# Email index range
EMAIL_START_INDEX = 140
EMAIL_END_INDEX = 145

# Load environment variables
dotenv.load_dotenv()
DOMAIN = os.getenv("TARGET_DOMAIN")
EMAIL_FARM_DOMAIN = os.getenv("EMAIL_FARM_DOMAIN")

def call_api(api_url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(api_url)
        page.wait_for_timeout(4000)
        response = page.content()
        if "error" in response: # Check for errors in the response
            print("Error occurred")
            print(response)
            raise Exception("API call failed")
        browser.close()

def get_email_address(index: int) -> str:
    return f"ff{index}%40{EMAIL_FARM_DOMAIN}"

def get_email_registration_api_url(email: str) -> str:
    return DOMAIN + '/includes/mailing_list/join-club.php?email_address=' + email

def request_email_registration(email: str):
    sign_up_api = get_email_registration_api_url(email)
    call_api(sign_up_api)
    print("Account Created for:", email)

def apply_delay(MIN:int = 60, MAX:int = 75):
    random_variance = random.uniform(MIN, MAX) # adding variance to avoid patterns
    time.sleep(random_variance)

if __name__ == "__main__":
    # automated email registration over a range of new email addresses
    for i in range(EMAIL_START_INDEX, EMAIL_END_INDEX):
        email = get_email_address(i)
        request_email_registration(email)
        if i < EMAIL_END_INDEX - 1:  # Avoid delay after the last email
            apply_delay()