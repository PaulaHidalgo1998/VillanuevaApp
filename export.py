import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def export_to_excel(personas, filename="personas.xlsx"):
    df = pd.DataFrame(personas, columns=["ID", "Nombre", "Apellidos", "Dinero", "Tipo Aportación"])
    df.to_excel(filename, index=False)

def export_to_pdf(base_datos, year):
    filename="villanueva_cuotas_personas_" + str(year) + ".pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40
    equivalencia_centimetro = 75
    valor_encabezado = 150
    valor_espaciado_little= 20
    valor_espaciado_big= 60

    count = 0

    c.drawString(valor_encabezado, y, "Cuotas ordinarias (40€)")
    for persona in base_datos.get_personas_by_tipo("Adulto"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))
        

    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "Cuotas más de 67 años (25€)")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Mayor 67"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))


    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "Cuotas de 12 a 17 años (15€)")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Joven"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "Niños menores de 12 años que portan la voluntad")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Menores 12"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "Aportaciones de distintos negocios")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Aportaciones negocios"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "Otras cantidades no consideradas cuotas")
    count = 0
    for persona in base_datos.get_personas_by_tipo("Cantidades no cuota"):
        y = valor_y(y, valor_espaciado_little, valor_espaciado_big, height, c)
        count += 1
        c.drawString(equivalencia_centimetro, y, str(count))
        c.drawString(equivalencia_centimetro*1.2, y, str(persona[2]) + ", " + persona[1])
        c.drawString(equivalencia_centimetro*5, y, str(persona[3]))

    y = valor_y(y, valor_espaciado_big, valor_espaciado_big, height, c)
    c.drawString(valor_encabezado, y, "GRACIAS A TODOS POR PARTICIPAR!")

    c.save()

def valor_y(previous_y, valor_espaciado, limite_espaciado, max_height, c):
    new_y = previous_y - valor_espaciado
    if new_y <= limite_espaciado:
        c.showPage()
        new_y = max_height - 40
    return new_y