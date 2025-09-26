# tests/test_pdf.py

import pytest
from backend.models.pdf_report import PDFReport
import os

def test_pdf_generation():
    filename = "test_report.pdf"
    pdf = PDFReport(filename=filename)
    pdf.add_title("Test PDF")
    pdf.add_paragraph("This is a test paragraph.")
    pdf.add_table([["Name", "Age"], ["John", 30]])
    output_file = pdf.save()
    assert os.path.exists(output_file)
    os.remove(output_file)  # Cleanup
