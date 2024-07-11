import pandas as pd

def import_from_excel(filename, db):
    df = pd.read_excel(filename)
    for _, row in df.iterrows():
        db.add_persona(row['Nombre'], row['Apellidos'], row['Dinero'], row['Tipo Aportación'])
