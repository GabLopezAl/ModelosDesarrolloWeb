from fastapi import APIRouter, HTTPException, status
from fastapi import Path
from pydantic import BaseModel
from typing import Optional
import pandas as pd

router= APIRouter()

# Definimos nuestro entidad clase que se usará como ejemplo

class User(BaseModel):
    matricula: Optional[int] = None
    pelicula_fav: Optional[str] = None

def peliculas(file_path: str) -> list[User]:
    df = pd.read_excel(file_path)
    pelis = [User(**row) for row in df.to_dict(orient="records")]
    return pelis

"""DELETE"""
@router.delete("/usersclass/{matricula}",status_code=status.HTTP_200_OK)
async def delete_user(matricula: int = Path(..., description="Matrícula del usuario a eliminar")):
    file_path = "peliculas.xlsx"
    users = peliculas(file_path)
    found = False

    usuarios_filtrados = []
    for user in users:
        if user.matricula == matricula:
            found = True
            continue
        usuarios_filtrados.append(user)

    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail={"message": "No se pudo eliminar el usuario"})

    excel_actualizado = pd.DataFrame([u.dict() for u in usuarios_filtrados])
    excel_actualizado.to_excel(file_path, index=False)

    return {"Usuario eliminado correctamente"}