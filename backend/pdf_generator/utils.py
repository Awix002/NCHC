from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_lab_report_pdf(report_data, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)

    # Add content to the PDF using ReportLab methods
    c.drawString(100, 750, "Lab Report")
    c.drawString(100, 730, "---------------------")
    
    y_coordinate = 700
    for key, value in report_data.items():
        c.drawString(100, y_coordinate, f"{key}: {value}")
        y_coordinate -= 20
    
    c.save()
