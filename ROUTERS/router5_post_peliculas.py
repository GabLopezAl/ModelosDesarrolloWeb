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


"""POST"""
@router.post("/usersclass/",status_code=status.HTTP_201_CREATED)
async def userclass(user: User):
    file_path = "peliculas.xlsx"
    lista_peliculas: list[User] = peliculas(file_path)

    for u in lista_peliculas:
        if u.matricula == user.matricula:
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE,detail={"message": "El alumno ya existe"})

    lista_peliculas.append(user)

    excel_actualizado = pd.DataFrame([u.dict() for u in lista_peliculas])
    excel_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Pelicula agregada correctamente", "usuario": user}
