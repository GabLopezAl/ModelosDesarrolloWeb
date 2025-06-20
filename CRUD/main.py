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


"""GET"""
@app.get("/usersclass/")
async def usersclass():
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    try:
        return list(users)
    except:
        return{"No se pudieron obtener los usuarios"}
    

"""POST"""
@app.post("/usersclass/")
async def userclass(user:User):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)

    # for index, saved_user in enumerate(users):
    #     if saved_user.matricula == user.matricula:
    #         return {"error": "El usuario ya existe"}
    #     else:
    #         users.append(user)
    #         return user
    # Verificar si ya existe el usuario
    if user.matricula in users["matricula"].astype(str).values:
        return {"error": "El usuario ya existe"}

    # Convertir el nuevo usuario en DataFrame
    new_user_df = pd.DataFrame([user.dict()])

    # Concatenar y guardar
    df_actualizado = pd.concat([users, new_user_df], ignore_index=True)
    df_actualizado.to_excel(file_path, index=False)
    

"""PUT"""
@app.put("/usersclass/")
async def userclass(user:User):
    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    found = False

    for index, saved_user in enumerate(users):
        if saved_user.matricula == user.matricula:
            users[index] = user
            found = True
    if not found:
        return {"error": "No se pudo actualizar el usuario"}
    else:
        return {"Registro actualizado correctamente"}
