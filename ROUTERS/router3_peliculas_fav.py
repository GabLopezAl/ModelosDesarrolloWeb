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

"""GET dada la matricula"""
@router.get("/usersclass/{matricula}",status_code=status.HTTP_200_OK)
async def usersclass(matricula: int):
    file_path = "peliculas.xlsx"
    users = peliculas(file_path)
    users = filter (lambda user: user.matricula == matricula, users)
    try:
        return list(users)
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail={"message": "No se puede obtener el alumno"})
        # return{"No se pudieron obtener los usuarios"}
    