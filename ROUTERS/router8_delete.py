from fastapi import APIRouter, HTTPException, status
from fastapi import Path
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


"""DELETE"""
@router.delete("/usersclass/{matricula}",status_code=status.HTTP_200_OK)
async def delete_user(matricula: int = Path(..., description="Matrícula del usuario a eliminar")):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    found = False

    usuarios_filtrados = []
    for user in users:
        if user.matricula == matricula:
            found = True
            continue
        usuarios_filtrados.append(user)

    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail={"message": "No se pudo eliminar el usuario"})
       # return {"error": "Usuario no encontrado"}

    excel_actualizado = pd.DataFrame([u.dict() for u in usuarios_filtrados])
    excel_actualizado.to_excel(file_path, index=False)

    return {"Usuario eliminado correctamente"}