# models/pdf_report.py

from fpdf import FPDF
import datetime

class PDFReport:
    def __init__(self, filename="health_report.pdf"):
        self.filename = filename
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def add_title(self, title):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(0, 10, title, ln=True, align="C")
        self.pdf.ln(10)

    def add_paragraph(self, text):
        self.pdf.set_font("Arial", '', 12)
        self.pdf.multi_cell(0, 10, text)
        self.pdf.ln(5)

    def add_table(self, data, col_widths=None):
        self.pdf.set_font("Arial", '', 12)
        if not data:
            return
        col_widths = col_widths or [40] * len(data[0])
        for row in data:
            for i, item in enumerate(row):
                self.pdf.cell(col_widths[i], 10, str(item), border=1)
            self.pdf.ln()

    def save(self):
        self.pdf.output(self.filename)
        return self.filename

# Example usage:
if __name__ == "__main__":
    report = PDFReport("example_report.pdf")
    report.add_title("Patient Health Report")
    report.add_paragraph("This report contains patient health details and analytics.")
    report.add_table([["Name", "Age", "Condition"], ["John Doe", 30, "Healthy"], ["Jane Doe", 28, "Flu"]])
    report.save()
    print("PDF report generated successfully.")
