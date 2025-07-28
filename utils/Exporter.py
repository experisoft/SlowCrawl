import pathlib
from utils.PdfGenerator import PdfGenerator

class Exporter:
    def __init__(self):
        self.PDF_FILE = "vouchers.pdf"
        self.STORE_FOLDER = "store"
        self.USED_VOUCHER_FILE = "used_vouchers.txt"

    def get_voucher_paths(self):
        return [str(file) for file in pathlib.Path(self.STORE_FOLDER).glob("*.png")]
    
    def add_voucher_to_used_list(self, voucher_file_name: str):
        with open(self.USED_VOUCHER_FILE, "a") as file:
            file.write(f"{voucher_file_name}\n")

    def delete_voucher_file(self, voucher_path: str):
        voucher_path = pathlib.Path(voucher_path)
        if voucher_path.exists():
            voucher_path.unlink()
        else:
            print(f"Voucher file {voucher_path} does not exist.")

    def mark_vouchers_as_used(self, voucher_file_names: [str]):
        for voucher_file_name in voucher_file_names:
            self.add_voucher_to_used_list(voucher_file_name)
            self.delete_voucher_file(voucher_file_name)

    def get_voucher_value_from_filename(self, voucher_file_name: str) -> str:
        try:
            return int(voucher_file_name.split("_")[-1].split(".")[0].replace("£", "").strip())
        except ValueError:
            print(f"Error parsing voucher value from filename: {voucher_file_name}")
            return 0

    def run(self):
        unused_voucher_paths = self.get_voucher_paths()
        pdf_generator = PdfGenerator(self.PDF_FILE)

        if not unused_voucher_paths:
            print("No vouchers found to export.")
            return
        
        accumulated_value = 0
        
        for voucher_path in unused_voucher_paths:
            pdf_generator.add_image_to_pdf(voucher_path)
            voucher_value = self.get_voucher_value_from_filename(pathlib.Path(voucher_path).name)
            accumulated_value += voucher_value

        pdf_generator.add_accumulated_value_text_to_top(accumulated_value)
        
        pdf_generator.save_pdf()
        print(f"Exported {len(unused_voucher_paths)} vouchers to {self.PDF_FILE}.")
        print(f"Total accumulated voucher value: £{accumulated_value}")

        self.mark_vouchers_as_used(unused_voucher_paths)