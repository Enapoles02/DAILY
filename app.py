import streamlit as st
import pandas as pd
import requests
import io

# Configuración de GitHub
GITHUB_REPO = "Enapoles02/DAILY"  # Reemplaza con tu usuario/repositorio
GITHUB_TOKEN = "TOKEN_DAILY"   # Genera un token en GitHub con permisos de escritura
DB_FILE = "users.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DB_FILE}"

# Función para obtener el contenido del archivo desde GitHub
def obtener_datos():
    try:
        response = requests.get(GITHUB_API_URL)
        if response.status_code == 200:
            content = response.json()
            csv_data = requests.get(content["download_url"]).text
            return pd.read_csv(io.StringIO(csv_data))
        else:
            return pd.DataFrame(columns=["Nombre", "Correo", "Área"])
    except:
        return pd.DataFrame(columns=["Nombre", "Correo", "Área"])

# Función para guardar el usuario en GitHub
def guardar_usuario(nombre, correo, area, password):
    df = obtener_datos()
    nuevo_usuario = pd.DataFrame([[nombre, correo, area]], columns=["Nombre", "Correo", "Área"])
    df = pd.concat([df, nuevo_usuario], ignore_index=True)

    # Convertir a CSV
    csv_data = df.to_csv(index=False)

    # Obtener el SHA del archivo (necesario para actualizar)
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha", "")

    # Subir cambios a GitHub
    payload = {
        "message": "Nuevo usuario registrado",
        "content": io.BytesIO(csv_data.encode()).getvalue().decode("latin1"),
        "branch": "main",
        "sha": sha
    }
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    requests.put(GITHUB_API_URL, json=payload, headers=headers)

# Interfaz de Streamlit
st.title("Portal de Registro")

# Formulario de Registro
with st.form("register_form"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    area = st.selectbox("Área", ["Finanzas", "TI", "Recursos Humanos", "Ventas", "Otro"])
    password = st.text_input("Contraseña", type="password")
    submit_button = st.form_submit_button("Registrar")

if submit_button:
    if nombre and correo and area and password:
        guardar_usuario(nombre, correo, area, password)
        st.success(f"Usuario {nombre} registrado exitosamente")
    else:
        st.error("Todos los campos son obligatorios")

# Sección protegida para ver usuarios registrados
clave = st.text_input("Ingresa la clave de acceso", type="password")

if clave == "Naec2828":
    st.success("Acceso permitido")
    df = obtener_datos()
    if not df.empty:
        st.dataframe(df)
    else:
        st.error("No hay usuarios registrados.")
