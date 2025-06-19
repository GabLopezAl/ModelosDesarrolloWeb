# Importamos librerías
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Creamos una instancia de FastAPI
app = FastAPI()

# Definimos nuestro entidad clase que se usará como ejemplo

class User(BaseModel):
    nombre_completo: Optional[str] = None
    matricula: Optional[int] = None
    edad: Optional[int] = None
    carrera: Optional[str] = None
    genero: Optional[str] = None
    semestre: Optional[int] = None
    porcentaje_carrera: Optional[float] = None
    facultad: Optional[str] = None
    materias_reprobadas: Optional[int] = None
    promedio: Optional[float] = None

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
    

"""MATRICULA"""
@app.get("/usersclass/matricula/{matr}")
async def userclass(matr:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.matricula == matr, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}


"""EDAD"""
@app.get("/usersclass/edad/{edad}")
async def userclass(edad:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.edad == edad, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""CARRERA"""
@app.get("/usersclass/carrera/{carrera}")
async def userclass(carrera:str):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.carrera == carrera, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""GENERO"""
@app.get("/usersclass/genero/{genero}")
async def userclass(genero:str):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.genero == genero, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""SEMESTRE"""
@app.get("/usersclass/semestre/{sem}")
async def userclass(sem:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.semestre == sem, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""Porcentaje de carrera"""
@app.get("/usersclass/porcentajeCarrera/{porcCarr}")
async def userclass(porcCarr:float):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.porcentaje_carrera == porcCarr, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}



"""FACULTAD"""
@app.get("/usersclass/facultad/{fac}")
async def userclass(fac:str):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.facultad == fac, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""MATERIAS REPROBADAS"""
@app.get("/usersclass/materiasReprob/{matRep}")
async def userclass(matRep:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.materias_reprobadas == matRep, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    

"""PROMEDIO"""
@app.get("/usersclass/promedio/{prom}")
async def userclass(prom:float):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.promedio >= prom, users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
    


"""GET por QUERY"""
"""NOMBRE y EDAD"""
@app.get("/usersclass2/")
async def usersclass(age:int, name: str):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.edad == age and user.nombre_completo == name,users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
"""http://127.0.0.1:8000/usersclass2/?age=21&name=LOPEZ%20ALVARADO%20ANGEL%20GABRIEL"""


"""MATRICULA"""
@app.get("/usersclass3/")
async def usersclass(matricula:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.matricula == matricula,users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}
"""http://127.0.0.1:8000/usersclass3/?matricula=202108321"""


"""CARRERA y EDAD"""
@app.get("/usersclass4/")
async def usersclass(matricula:int):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    users = filter (lambda user: user.matricula == matricula,users)
    try:
        return list(users)
    except:
        return{"No se ha encontrado al usuario"}