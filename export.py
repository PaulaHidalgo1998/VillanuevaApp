import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_excel(personas, filename="personas.xlsx"):
    df = pd.DataFrame(personas, columns=["ID", "Nombre", "Apellidos", "Dinero", "Tipo Aportación"])
    df.to_excel(filename, index=False)

def export_to_pdf(base_datos, filename="personas.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    equivalencia_centimetro = 75
    valor_encabezado = 150
    valor_espaciado_little= 20
    valor_espaciado_big= 80

    count = 0

    c.drawString(valor_encabezado, y, "Cuotas ordinarias (40€)")
    for persona in base_datos.get_personas_by_tipo("Adulto"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))
        

    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "Cuotas más de 67 años (25€)")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Mayor 67"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))


    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "Cuotas de 12 a 17 años (15€)")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Joven"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "Niños menores de 12 años que portan la voluntad")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Menores 12"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "Aportaciones de distintos negocios")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Aportaciones negocios"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "Otras cantidades no consideradas cuotas")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Cantidades no cuota"):
        y -= valor_espaciado_little
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y -= valor_espaciado_big
    c.drawString(valor_encabezado, y, "GRACIAS A TODOS POR PARTICIPAR!")

    c.save()
