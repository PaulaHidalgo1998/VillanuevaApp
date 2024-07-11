import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_excel(personas, filename="personas.xlsx"):
    df = pd.DataFrame(personas, columns=["ID", "Nombre", "Apellidos", "Dinero", "Tipo Aportación"])
    df.to_excel(filename, index=False)

def export_to_pdf(personas, filename="personas.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40

    for persona in personas:
        c.drawString(30, y, str(persona))
        y -= 20

    c.save()
