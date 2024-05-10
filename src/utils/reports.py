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
        for index in range(10):
            pdf.image(f"images/top10_{year}_{index}.png", w=200)
        pdf.add_page()
        pdf.header(f'Top 5 Artists of the Year {year}')
        pdf.image(f"images/top5_{year}.png", w=170)
    else:
        pdf.set_font(FONT, 'B', 16)
        pdf.header('Summary Tracks by years')
        pdf.image("images/summary.png", w=170)
        pdf.add_page()
        pdf.header('Top 10 Songs of All Time')
        for index in range(10):
            pdf.image(f"images/top10_{index}.png", w=200)
        pdf.add_page()
        pdf.header('Top 5 Artists of All Time')
        pdf.image("images/top5.png", w=170)
    
    return pdf.output(dest='S').encode('latin-1')

def generate_excel_report(year=''):
    wb = openpyxl.Workbook()
    if year:
        ws = wb.active
        ws['A1'] = 'Hello World!'
        wb.save('report.xlsx')
