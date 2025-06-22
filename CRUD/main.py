# Importamos librerías
import pandas as pd
from fastapi import FastAPI
from fastapi import Path
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
async def userclass(user: User):
    file_path = "Registros.xlsx"

    usuarios: list[User] = estudiantes(file_path)

    for u in usuarios:
        if u.matricula == user.matricula:
            return {"error": "El usuario ya existe"}

    usuarios.append(user)

    df_actualizado = pd.DataFrame([u.dict() for u in usuarios])
    df_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Usuario agregado correctamente", "usuario": user}

    

"""PUT"""
@app.put("/usersclass/")
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
        return {"error": "No se pudo actualizar el usuario"}

    df_actualizado = pd.DataFrame([u.dict() for u in users])
    df_actualizado.to_excel(file_path, index=False)

    return {"mensaje": "Registro actualizado correctamente", "usuario": user}


"""DELETE"""
@app.delete("/usersclass/{matricula}")
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
        return {"error": "Usuario no encontrado"}

    df_actualizado = pd.DataFrame([u.dict() for u in usuarios_filtrados])
    df_actualizado.to_excel(file_path, index=False)

    return {"Usuario eliminado correctamente"}
