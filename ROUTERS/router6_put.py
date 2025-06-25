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


"""PUT"""
@router.put("/usersclass/",status_code=status.HTTP_200_OK)
async def userclass(user: User):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    found = False

    for index, saved_user in enumerate(users):
        if saved_user.matricula == user.matricula:
            users[index] = user
            found = True
            break

    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail={"message": "No se pudo actualizar el usuario"})

    excel_actualizado = pd.DataFrame([u.dict() for u in users])
    excel_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Registro actualizado correctamente", "usuario": user}

