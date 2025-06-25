#Importamos el framework fastapi a nuestro entorno de trabajo
from fastapi import FastAPI, Request
#Importamos la clase staticfiles para recursos estáticos****
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#Creamos un objeto a partir de la clase FastAPI
app= FastAPI()


#Creamos una app para acceder al directorio de recursos estaticos***
app.mount("/images", StaticFiles(directory="static"), name="static")
# En el explorador colocamos el siguiente path para cargar recurso estático:
# http://127.0.0.1:8000/static_resources/images/leopardo.jpg



# Configurar templates Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/user_0", response_class=HTMLResponse)
def get_user_0(request: Request):
    user_0 = {
        "nombre": "Alfredo",
        "apellido": "García",
        "foto_url": "/static_resources/images/User_0.jpg"
    }
    return templates.TemplateResponse("user_0.html", {"request": request, "user_0": user_0})

#http://127.0.0.1:8000/user_0

#Utilizamos la (instancia) función get del framework FastAPI
@app.get("/")

#creamos la función asincrona "imprimir"
async def imprimir():
    return "Hola estudiantes"


#Levantamos el server Uvicorn
#-uvicorn 6_StaticResources:app --reload-
# En el explorador colocamos la raiz de la ip: http://127.0.0.1:8000



#Documentación con Swagger:  http://127.0.0.1:8000/docs
#Documentación con Redocly:  http://127.0.0.1:8000/redoc