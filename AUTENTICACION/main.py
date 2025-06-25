from fastapi import FastAPI, Depends, HTTPException, status, Request
#Importamos pydantic para obtener una entidad que pueda definir usuarios
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#Importamos librería jwt
from jose import jwt, JWTError
#Importamos libreria passlib (algoritmo de encriptación)
from passlib.context import CryptContext
#Importamos libreria de fechas para la expiración del token
from datetime import datetime, timedelta

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import pandas as pd

#Implementamos algoritmo de haseo para encriptar contraseña
ALGORITHM = "HS256"
#Duración de autenticación 
ACCESS_TOKEN_DURATION= 1
#Creamos un secret
SECRET="123456789"

#Creamos un objeto o instancia a partir de la clase FastAPI
app= FastAPI()

#Autenticación por contraseña para eso:
#Creamos un endpoint llamado "login"
oauth2=OAuth2PasswordBearer(tokenUrl="login")

#Creamos contexto de encriptación para eso importamos libreria passlib y elegimos algoritmo de incriptación "bcrypt"
#Utilizamos bcrypt generator para encriptar nuestras contraseñas
crypt= CryptContext(schemes="bcrypt")

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
    contrasena: Optional[str] = None

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
        "Promedio": "promedio",
        "Contrasena": "contrasena"
    })
    users = [User(**row) for row in df.to_dict(orient="records")]
    return users

#Definimos la clase para el usuario de base de datos 
class UserDB(User):
    password:str

file_path = "Registros.xlsx"
users = estudiantes(file_path)

#1 Función para regresar el usuario completo de la base de datos (users_db), con contraseña encriptada
def search_user_db(username:str):
    
    if username in users:
        return UserDB(**users[username]) #** devuelve todos los parámetros del usuario que coincida con username

#4 Función final para devolver usuario a la solicitud del backend   
def search_user(username:str):
    if username in users:
        return User(**users[username])
    
#2 Esta es la dependencia para buscar al usuario
async def auth_user(token:str=Depends(oauth2)):
    try:
        username= jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")

    return search_user(username) #Esta es la entrega final, usuario sin password
