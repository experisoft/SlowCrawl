import pathlib
from fpdf import FPDF
from playwright.sync_api import sync_playwright

STORE_FOLDER = "store"
USED_VOUCHER_FILE = f"{STORE_FOLDER}/used_vouchers.txt"
PDF_FILE = "vouchers.pdf"
SCREENSHOT_PATH = "screenshot.png"
VOUCHER_WIDTH = 45
VOUCHER_HEIGHT = 55

if not pathlib.Path(STORE_FOLDER).exists():
    pathlib.Path(STORE_FOLDER).mkdir(parents=True)

if not pathlib.Path(USED_VOUCHER_FILE).exists():
    with open(USED_VOUCHER_FILE, "w") as file:
        file.write("")

def voucher_is_used(voucher_file_name: str) -> bool:
    try:
        with open(USED_VOUCHER_FILE, "r") as file:
            used_vouchers = file.read().splitlines()
        return voucher_file_name in used_vouchers
    except FileNotFoundError:
        return False

def screenshot_active_vouchers(page_url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(page_url)

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

        page.screenshot(path=SCREENSHOT_PATH)

        voucher_elements = page.query_selector_all("#active_vouchers .col-lg-3.col-md-4.col-sm-4.col-xs-12")

        if not voucher_elements:
            print("No active vouchers found on the page.")
            return

        print(f"Found {len(voucher_elements)} active vouchers.")

        for i, voucher in enumerate(voucher_elements):
            voucher_title = voucher.query_selector("h3").inner_text()
            voucher_ammount = voucher.query_selector("h4").inner_text()

            words = voucher_ammount.split()
            words = [word for word in words if word.startswith("£")]
            voucher_ammount = words[1] if len(words) > 1 else "N/A"

            print(f"Voucher {i + 1}: {voucher_title} - {voucher_ammount}")
            filename = f"{STORE_FOLDER}/{voucher_title}({voucher_ammount}).png"

            if voucher_is_used(filename):
                print(f"Voucher {voucher_title} ({voucher_ammount}) has already been used. Skipping screenshot.")
                continue

            voucher.screenshot(path=filename)
            print(f"Screenshot saved: {filename}")

        browser.close()

def get_list_of_links(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]
    
def mark_voucher_as_used(voucher_file_name: str):
    with open(USED_VOUCHER_FILE, "a") as file:
        file.write(f"{voucher_file_name}\n")
    # delete the voucher file after marking it as used
    voucher_path = pathlib.Path(STORE_FOLDER) / voucher_file_name
    if voucher_path.exists():
        voucher_path.unlink()
        print(f"Deleted voucher file: {voucher_file_name}")
    print(f"Marked voucher {voucher_file_name} as used.")
    
def create_pdf_from_screenshots():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    # add images
    current_x = pdf.l_margin
    current_y = pdf.t_margin
    for file in pathlib.Path(STORE_FOLDER).glob("*.png"):
        
        if current_x >= pdf.w - pdf.r_margin - VOUCHER_WIDTH:
            current_x = pdf.l_margin
            current_y += VOUCHER_HEIGHT
        if current_y >= pdf.h - pdf.b_margin - VOUCHER_HEIGHT:
            pdf.add_page()
            current_x = pdf.l_margin
            current_y = pdf.t_margin
        pdf.set_xy(current_x, current_y)
        pdf.image(file, x=current_x, y=current_y, w=VOUCHER_WIDTH, h=VOUCHER_HEIGHT)
        current_x += VOUCHER_WIDTH

        mark_voucher_as_used(file.name)

    pdf.output(PDF_FILE)
    
if __name__ == "__main__":
    links = get_list_of_links("links.txt")
    # for link in links:
    #     screenshot_active_vouchers(link)

    create_pdf_from_screenshots()

    