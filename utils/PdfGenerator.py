from fpdf import FPDF

class PdfGenerator:
    def __init__(self, output_path):
        self.OUTPUT_PATH = output_path
        self.VOUCHER_WIDTH = 45
        self.VOUCHER_HEIGHT = 55
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font('helvetica', size=12)

    def get_next_cursor_position(self, current_x, current_y):

        current_x += self.VOUCHER_WIDTH

        if current_x + self.VOUCHER_WIDTH > self.pdf.w - self.pdf.r_margin:
            current_x = self.pdf.l_margin
            current_y += self.VOUCHER_HEIGHT

        elif current_y + self.VOUCHER_HEIGHT > self.pdf.h - self.pdf.b_margin:
            self.pdf.add_page()
            current_x = self.pdf.l_margin
            current_y = self.pdf.t_margin

        
        return current_x, current_y
        
    def move_cursor(self):
        current_x, current_y = self.pdf.get_x(), self.pdf.get_y()
        current_x, current_y = self.get_next_cursor_position(current_x, current_y)
        self.pdf.set_xy(current_x, current_y)

    def add_image_to_pdf(self, image_path):
        self.pdf.image(image_path, w=self.VOUCHER_WIDTH, h=self.VOUCHER_HEIGHT, x=self.pdf.get_x(), y=self.pdf.get_y())
        self.move_cursor()

    def add_accumulated_value_text_to_top(self, accumulated_value):
        page_bottom = self.pdf.h - self.pdf.b_margin
        self.pdf.set_font('helvetica', 'B', size=10)
        self.pdf.set_xy(self.pdf.l_margin, page_bottom - 10)
        self.pdf.cell(0, 0, f"Total accumulated voucher value: £{accumulated_value}", ln=True, align='C')

    def save_pdf(self):
        self.pdf.output(self.OUTPUT_PATH)