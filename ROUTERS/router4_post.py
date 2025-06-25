from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import pandas as pd

router= APIRouter()

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


"""POST"""
@router.post("/usersclass/",status_code=status.HTTP_201_CREATED)
async def userclass(user: User):
    file_path = "Registros.xlsx"

    usuarios: list[User] = estudiantes(file_path)

    for u in usuarios:
        if u.matricula == user.matricula:
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE,detail={"message": "El alumno ya existe"})

    usuarios.append(user)

    excel_actualizado = pd.DataFrame([u.dict() for u in usuarios])
    excel_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Usuario agregado correctamente", "usuario": user}
