import pathlib
import PdfGenerator

class Exporter:
    def __init__(self):
        self.PDF_FILE = "vouchers.pdf"
        self.STORE_FOLDER = "store"
        self.USED_VOUCHER_FILE = f"{self.STORE_FOLDER}/used_vouchers.txt"

    def get_voucher_paths(self):
        return [str(file) for file in pathlib.Path(self.STORE_FOLDER).glob("*.png")]
    
    def add_voucher_to_used_list(self, voucher_file_name: str):
        with open(self.USED_VOUCHER_FILE, "a") as file:
            file.write(f"{voucher_file_name}\n")
        print(f"Added voucher {voucher_file_name} to used list.")

    def delete_voucher_file(self, voucher_file_name: str):
        voucher_path = pathlib.Path(self.STORE_FOLDER) / voucher_file_name
        if voucher_path.exists():
            voucher_path.unlink()
            print(f"Deleted voucher file: {voucher_file_name}")
        else:
            print(f"Voucher file {voucher_file_name} does not exist.")

    def mark_vouchers_as_used(self, voucher_file_names: str[]):
        for voucher_file_name in voucher_file_names:
            self.add_voucher_to_used_list(voucher_file_name)
            self.delete_voucher_file(voucher_file_name)

    def run(self):
        unused_voucher_paths = self.get_voucher_paths()
        pdf_generator = PdfGenerator(self.PDF_FILE)

        if not unused_voucher_paths:
            print("No vouchers found to export.")
            return
        
        for voucher_path in unused_voucher_paths:
            pdf_generator.add_image_to_pdf(voucher_path)

        pdf_generator.save_pdf()
        print(f"Exported {len(unused_voucher_paths)} vouchers to {self.PDF_FILE}.")    

        self.mark_vouchers_as_used(unused_voucher_paths)