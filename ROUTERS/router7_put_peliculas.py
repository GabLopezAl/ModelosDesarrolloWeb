from fastapi import APIRouter, HTTPException, status
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

"""PUT"""
@router.put("/usersclass/",status_code=status.HTTP_200_OK)
async def userclass(user: User):
    file_path = "peliculas.xlsx"
    lista_peliculas = peliculas(file_path)
    found = False

    for index, saved_user in enumerate(lista_peliculas):
        if saved_user.matricula == user.matricula:
            lista_peliculas[index] = user
            found = True
            break

    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail={"message": "No se pudo actualizar el usuario"})
        # return {"error": "No se pudo actualizar el usuario"}

    excel_actualizado = pd.DataFrame([u.dict() for u in lista_peliculas])
    excel_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Registro actualizado correctamente", "usuario": user}
