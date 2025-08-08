from playwright.sync_api import sync_playwright
import pathlib

class Scraper:
    def __init__(self):
        self.STORE_FOLDER = "store"
        self.USED_VOUCHER_FILE = f"used_vouchers.txt"
    
    def is_voucher_used(self, voucher_file_name: str) -> bool:
        if not pathlib.Path(self.USED_VOUCHER_FILE).exists():
            return False

        with open(self.USED_VOUCHER_FILE, "r", encoding="utf-8") as file:
            used_vouchers = file.readlines()
        return pathlib.Path(voucher_file_name).name in [line.strip() for line in used_vouchers]

    def click_accept_cookies(self, page):
        try:
            cookie_banner = page.locator("#cookie_banner")
            if cookie_banner.is_visible():
                print("Cookie banner detected. Attempting to accept...")
                page.click("#cookie_accept")
                cookie_banner.wait_for(state="hidden", timeout=10000)
                print("Cookie banner accepted and closed.")
            else:
                print("No cookie banner visible or already dismissed.")
        except Exception as e:
            print(f"Error handling cookie banner: {e}")

    def get_voucher_elements(self, page):
        return page.query_selector_all("#active_vouchers .col-lg-3.col-md-4.col-sm-4.col-xs-12")
    
    def get_voucher_text(self, voucher):
        voucher_code = voucher.query_selector("h3").inner_text()
        voucher_amount = voucher.query_selector("h4").inner_text().split()[-1]
        voucher_amount = voucher_amount.replace("£", "").strip()
        return voucher_code, voucher_amount

    def get_voucher_file_name(self, voucher_code, voucher_amount):
        return f"{voucher_code}_{voucher_amount}.png"
    
    def screenshot_voucher_elements(self, voucher_elements):
        if not voucher_elements:
            print("No active vouchers found on the page.")
            return
        
        print(f"Found {len(voucher_elements)} active vouchers.")

        for i, voucher in enumerate(voucher_elements):
            voucher_code, voucher_amount = self.get_voucher_text(voucher)
            voucher_file_name = self.get_voucher_file_name(voucher_code, voucher_amount)

            if not self.is_voucher_used(voucher_file_name):
                voucher.screenshot(path=f"{self.STORE_FOLDER}/{voucher_file_name}")
                print(f"Saved screenshot for voucher: {voucher_file_name}")
            else:
                print(f"Voucher {voucher_file_name} has already been used.")

    def screenshot_active_vouchers(self, page_url: str):
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(page_url)

                self.click_accept_cookies(page)

                voucher_elements = self.get_voucher_elements(page)

                self.screenshot_voucher_elements(voucher_elements)
            finally:
                browser.close()
                print("Browser closed.")