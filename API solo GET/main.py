# Importamos librerías
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Creamos una instancia de FastAPI
app = FastAPI()

# Definimos nuestro entidad clase que se usará como ejemplo

class User(BaseModel):
    nombre_completo:str
    matricula: int
    edad: int
    carrera: str
    genero: str
    semestre: int
    porcentaje_carrera: float
    facultad: str
    materias_reprobadas: int
    promedio: float

# Leer Excel y convertir a lista de objetos User
def estudiantes(file_path: str) -> list[User]:
    df = pd.read_excel(file_path)
    # Renombramos las columnas del Excel para que coincidan con el modelo
    df = df.rename(columns={
        "Nombre Completo": "nombre_completo",
        "Matricula": "matricula",
        "Edad": "edad",
        "Carrera": "carrera",
        "Genero": "genero",
        "Semestre": "semestre",
        "Porcentaje de carrera": "porcentaje_carrera",
        "Facultad": "facultad",
        "Materias Reprobadas": "materias_reprobadas",
        "Promedio": "promedio"
    })
    users = [User(**row) for row in df.to_dict(orient="records")]
    return users

# Path con un solo nivel

# Primero
@app.get("/estudiantes")
async def students():
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    return users

# Segundo
@app.get("/carreras")
async def carreras():
    file_path = "Registros.xlsx"
    df = pd.read_excel(file_path)
    carreras_unicas = df["Carrera"].unique().tolist()

    return {"Carreras": carreras_unicas}

# Tercero
@app.get("/generos")
async def carreras():
    file_path = "Registros.xlsx"
    df = pd.read_excel(file_path)
    carreras_unicas = df["Genero"].unique().tolist()

    return {"Generos": carreras_unicas}

# Cuarto
@app.get("/semestres")
async def carreras():
    file_path = "Registros.xlsx"
    df = pd.read_excel(file_path)
    carreras_unicas = sorted(df["Semestre"].unique().tolist())

    return {"Semestres": carreras_unicas}