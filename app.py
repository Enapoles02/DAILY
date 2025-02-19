import streamlit as st
import pandas as pd
import requests
import os
import base64

# Configuración de GitHub
GITHUB_REPO = "Enapoles02/DAILY"  # Cambia esto si tu repo es diferente
CSV_FILE = "users.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE}"
WORKFLOW_URL = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/update_users.yml/dispatches"
GITHUB_TOKEN = os.getenv("TOKEN_DAILY")  # Secreto en GitHub

# Función para obtener el archivo CSV desde GitHub
def obtener_usuarios():
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        content = response.json()
        csv_data = base64.b64decode(content["content"]).decode("utf-8")
        return pd.read_csv(pd.io.common.StringIO(csv_data))
    return pd.DataFrame(columns=["Usuario", "Contraseña"])  # Si falla, devuelve un CSV vacío

# Función para guardar el usuario en GitHub
def guardar_usuario(usuario, password):
    df = obtener_usuarios()
    
    if usuario in df["Usuario"].values:
        return False  # No duplicar usuarios

    nuevo_usuario = pd.DataFrame([[usuario, password]], columns=["Usuario", "Contraseña"])
    df = pd.concat([df, nuevo_usuario], ignore_index=True)

    csv_data = df.to_csv(index=False).encode()
    content_encoded = base64.b64encode(csv_data).decode("utf-8")

    # Obtener el SHA del archivo (si ya existe)
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha", "")

    # Subir el nuevo CSV a GitHub
    payload = {
        "message": "Actualización de usuarios desde Streamlit",
        "content": content_encoded,
        "branch": "main",
        "sha": sha
    }
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.put(GITHUB_API_URL, json=payload, headers=headers)

    # 🚀 Disparar el workflow después de guardar el usuario
    if response.status_code in [200, 201]:
        requests.post(
            WORKFLOW_URL,
            headers={"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"},
            json={"ref": "main"}
        )

    return response.status_code in [200, 201]

# ---- INTERFAZ DE STREAMLIT ----
st.title("Daily Huddle App")

st.subheader("Registro de Usuario")

usuario_nuevo = st.text_input("Usuario")
password_nuevo = st.text_input("Contraseña", type="password")
boton_registro = st.button("Registrar")

if boton_registro:
    if usuario_nuevo and password_nuevo:
        if guardar_usuario(usuario_nuevo, password_nuevo):
            st.success("Usuario registrado con éxito.")
        else:
            st.error("El usuario ya existe. Intenta con otro nombre.")
    else:
        st.error("Debes ingresar un usuario y contraseña.")
