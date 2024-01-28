# from pandas import pd as pd
import pandas as pd
from sklearn import metrics
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from config.db_config import get_db_connection
# from models.user_model import User, Login, add_user

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse


app = FastAPI()
origins = [
    "http://localhost:5173"
]

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def index():
    html_address = "./templates/public/index.html"
    return FileResponse(html_address, status_code=200)


# Login user
@app.get("/login_user", response_class=HTMLResponse)
def login_user():
    html_address = "./templates/login/login.html"
    return FileResponse(html_address, status_code=200)

# add_user_router


@app.get("/add_user_r", response_class=HTMLResponse)
def add_user_r():
    html_address = "./templates/register/register.html"
    return FileResponse(html_address, status_code=200)


# Información
@app.get("/informacion", response_class=HTMLResponse)
def informacion():
    html_address = "./templates/user/informacion.html"
    return FileResponse(html_address, status_code=200)


@app.post("/index")
async def index(request: Request, correo: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuario WHERE correo = %s AND password = %s", (correo, password))
    user = cursor.fetchone()

    if user:
        # Lógica para almacenar datos en sesión (puedes adaptar esto según tus necesidades)
        html_address = "./templates/user/infor.html"
        return FileResponse(html_address, status_code=200)
    else:
        login = "./templates/login/login.html"
        return FileResponse(login, status_code=200)


@app.post('/register')  # Registro
async def register(request: Request,
                   nombre: str = Form(...),
                   apellido: str = Form(...),
                   tipo_documento: str = Form(...),
                   celular: int = Form(...),
                   identificacion: int = Form(...),
                   edad: int = Form(...),
                   peso: int = Form(...),
                   correo: str = Form(...),
                   password: str = Form(...),
                   # ID del rol con un valor predeterminado de 1
                   id_rol: int = Form(1)):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT * FROM usuario WHERE correo = %s""",
                       (correo,))  # Comprobar si exite el usuario
        user = cursor.fetchone()
        if user:
            msg = 'usuario existente'
            return JSONResponse(content={"msg": msg})

        else:
            cursor.execute("""INSERT INTO usuario (nombre, apellido, 
                               tipo_documento, celular, identificacion,
                               edad, peso, correo, password, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (nombre, apellido, tipo_documento, celular,
                            identificacion, edad, peso, correo, password, id_rol))

            conn.commit()
            html_address = "./templates/user/infor.html"
            return FileResponse(html_address, status_code=200)

    except Exception as e:
        # Manejar errores aquí
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        conn.close()
        cursor.close()


@app.get('/ai')
async def ai():
    address_ai = "./templates/ai/index_ai.html"
    return FileResponse(address_ai, status_code=200)


# #Prediction case


@app.post('/predicction')
async def predicction(request: Request, clase: str = Form(...), menopausia: int = Form(...), ubicacion: int = Form(...), cambios: int = Form(...), cambios_peso: int = Form(...),):
    seno = seno

    file_path = 'data/breast-cancer.data'
    df = pd.read_csv(file_path)
    df.info()
    df['clase'].unique()
    df.head(10)
    df['clase'].unique()

    if menopausia == 'no-recurrence-events':
        recurrent = 0    # Cargar un conjunto de datos de ejemplo, por ejemplo, el conjunto de datos de iris
    else:
        no_recurrent = 1

    df.head(10)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    # Dividir el conjunto de datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=99)

    # Crear un clasificador k-NN con, por ejemplo, k=3
    knn = KNeighborsClassifier(n_neighbors=2)
    # Ajustar el modelo con los datos de entrenamiento
    knn.fit(X_train, y_train)
    # Realizar predicciones en el conjunto de prueba
    y_pred = knn.predict(X_test)

    # Evaluar la precisión del modelo
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f'Precisión del modelo: {accuracy}')
    # Realizar una predicción para un nuevo conjunto de características (nueva instancia)
    # Asegúrate de ajustar las características según tu conjunto de datos

    # Ajusta los valores de las características según tu conjunto de datos
    new_data = [['no-recurrence-events', '40-49', 'ge40',
                 '20-24', '0-2', 'no', 1, 'left', 'left_low']]
    prediction = knn.predict(new_data)
    print(f'Predicción para nuevas características: {prediction}')


@app.get('/logout')
async def logout():
    logoutt = "./templates/login/login.html"
    return FileResponse(logoutt, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="12.0.0.1", port=5000)
