#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import FastAPI, Request, HTTPException, status
#Importamos la clase staticfiles para recursos estáticos****
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import pandas as pd

#Creamos un objeto a partir de la clase FastAPI
app= FastAPI()

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


#Creamos una app para acceder al directorio de recursos estaticos***
app.mount("/images/", StaticFiles(directory="images"), name="static")
# En el explorador colocamos el siguiente path para cargar recurso estático:
# http://127.0.0.1:8000/static_resources/images/leopardo.jpg



# Configurar templates Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/user_0/{matricula}", response_class=HTMLResponse,status_code=status.HTTP_200_OK)
def get_user_0(request: Request, matricula: int):

    file_path = "Registros.xlsx"
    users = estudiantes(file_path)
    
    user_list = list(filter(lambda user: user.matricula == matricula, users))
    if not user_list:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_0 = user_list[0]
    user_0_dict = user_0.dict()
    user_0_dict["foto_url"] = f"/images/{user_0.matricula}.jpg"


    return templates.TemplateResponse("users.html", {
        "request": request,
        "user_0": user_0_dict
    })
#http://127.0.0.1:8000/user_0/202148248



#Documentación con Swagger:  http://127.0.0.1:8000/docs
#Documentación con Redocly:  http://127.0.0.1:8000/redoc