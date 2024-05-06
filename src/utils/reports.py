from fpdf import FPDF
import openpyxl
from .plots import create_spider_plots_pdf

FONT = 'Arial'

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(10, 10, 10)
        self.background = None
        self.year = None
    
    def header(self, title=''):
        self.set_font(FONT, 'B', 24)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, 'I', 8)
        self.cell(0, 10, '%s' % self.page_no(), 0, 0, 'R')

    def set_background(self, image_path):
        self.background = image_path

    def set_year(self, year):
        self.year = year

    def first_page(self, year=''):
        self.set_background('public/PDF_background.png')
        self.add_page()
        if self.background:
            self.image(self.background, 0, 0, self.w, self.h)
        self.set_y(115)
        self.set_font(FONT, 'B', 85)
        self.cell(0, 5, '      Spotify', 0, 1, 'C')
        if year:
            self.set_y(150)
            self.set_font(FONT, '', 30)
            self.cell(0, 5, '      ANNUAL REPORT', 0, 1, 'C')
            self.set_y(260)
            self.set_font(FONT, 'I', 35)
            self.cell(0, 5, '         YEAR', 0, 1, 'L')
            self.set_y(260)
            self.cell(0, 5, year + '       ', 0, 1, 'R')
        else:
            self.set_y(150)
            self.set_font(FONT, '', 30)
            self.cell(0, 5, '  FULL REPORT', 0, 1, 'C')

def generate_pdf_report(year=''):
    pdf = PDFReport()
    pdf.first_page(year)

    pdf.set_year(year)
    pdf.add_page()

    if year:
        pdf.set_font(FONT, 'B', 16)
        pdf.header(f'Top 10 Songs of the Year {year}')
        images = create_spider_plots_pdf(int(year))
        for image in images:
            pdf.image(image.getvalue(), w=200, h=200)
    else:
        pdf.set_font(FONT, 'B', 16)
        pdf.header('Top 10 Songs of All Time')
        images = create_spider_plots_pdf(all_tracks=True)
        for image in images:
            pdf.image(image.getvalue(), w=200, h=200)
    
    return pdf.output(dest='S').encode('latin-1')

def generate_excel_report(year=''):
    wb = openpyxl.Workbook()
    if year:
        ws = wb.active
        ws['A1'] = 'Hello World!'
        wb.save('report.xlsx')
