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

def estudiantes(file_path: str) -> list[User]:
    df = pd.read_excel(file_path)
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


"""GET por PATH para cada columna (atributo)"""
"""Nombre completo"""
@app.get("/usersclass/user_name/{nomComp}")
async def userclass(nomComp:str):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.nombre_completo == nomComp, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}

# # Path con un solo nivel

# # Primero
# @app.get("/estudiantes")
# async def students():
#     file_path = "Registros.xlsx"
#     users = estudiantes(file_path)
#     return {"Alumnos registrados": users}

# # Segundo
# @app.get("/carreras")
# async def carreras():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     carreras_unicas = df["Carrera"].unique().tolist()

#     return {"Carreras": carreras_unicas}

# # Tercero
# @app.get("/generos")
# async def generos():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     carreras_unicas = df["Genero"].unique().tolist()

#     return {"Generos": carreras_unicas}

# # Cuarto
# @app.get("/semestres")
# async def semestres():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     carreras_unicas = sorted(df["Semestre"].unique().tolist())

#     return {"Semestres": carreras_unicas}


# # Path con solo dos niveles

# # Primero
# @app.get("/estudiantes/mujeres")
# async def estudMujeres():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     estud_mujeres = df[df["Genero"] == "FEMENINO"]

#     return  estud_mujeres.to_dict(orient="records")


# # Segundo
# @app.get("/estudiantes/hombres")
# async def estudHombres():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     estud_hombres = df[df["Genero"] == "MASCULINO"]

#     return  estud_hombres.to_dict(orient="records")


# # Tercero
# @app.get("/estudiantes/veinteaños")
# async def estudVeinteAños():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     edad_veinte = df[df["Edad"] == 20]

#     return  edad_veinte.to_dict(orient="records")


# # Path con solo tres niveles

# # Primero
# @app.get("/estudiantes/ITI/promedio")
# async def estudITIProm():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     carrera = df[df["Carrera"] == "ITI"]
#     promedio = carrera[["Nombre Completo","Carrera","Promedio"]]
#     return  promedio.to_dict(orient="records")


# # Segundo
# @app.get("/estudiantes/masculinos/octavosemestre")
# async def estudMascOctaSem():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     gen_sem = df[(df["Genero"] == "MASCULINO") & (df["Semestre"] == 8)]
#     promedio = gen_sem[["Nombre Completo","Genero","Semestre"]]
#     return  promedio.to_dict(orient="records")


# # Tercero
# @app.get("/estudiantes/ICC/porcentajecarrera")
# async def estudICCPorcCarrera():
#     file_path = "Registros.xlsx"
#     df = pd.read_excel(file_path)
#     carrera = df[df["Carrera"] == "ICC"]
#     procentaje = carrera[["Nombre Completo","Carrera","Porcentaje de carrera"]]
#     return  procentaje.to_dict(orient="records")