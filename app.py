import streamlit as st
import pandas as pd
import requests
import os
import base64

# Configuración de GitHub
GITHUB_REPO = "Enapoles02/DAILY"
CSV_FILE = "users.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE}"
GITHUB_TOKEN = os.getenv("TOKEN_DAILY")

# Función para obtener `users.csv` actualizado desde GitHub
def obtener_usuarios():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code == 200:
        content = response.json()
        csv_data = base64.b64decode(content["content"]).decode("utf-8")
        return pd.read_csv(pd.io.common.StringIO(csv_data))
    
    return pd.DataFrame(columns=["Usuario", "Contraseña"])  # Si no hay archivo, devuelve un CSV vacío

# Función para registrar un usuario en GitHub
def guardar_usuario(usuario, password):
    df = obtener_usuarios()

    usuario = usuario.strip().lower()
    df["Usuario"] = df["Usuario"].astype(str).str.strip().str.lower()

    if usuario in df["Usuario"].values:
        return False  # Ya existe el usuario

    nuevo_usuario = pd.DataFrame([[usuario, password]], columns=["Usuario", "Contraseña"])
    df = pd.concat([df, nuevo_usuario], ignore_index=True)

    csv_data = df.to_csv(index=False).encode()
    content_encoded = base64.b64encode(csv_data).decode("utf-8")

    # Obtener el SHA del archivo (necesario para actualizarlo)
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha", "")

    # Subir archivo a GitHub
    payload = {
        "message": "Actualización de usuarios desde Streamlit",
        "content": content_encoded,
        "branch": "main",
        "sha": sha
    }
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.put(GITHUB_API_URL, json=payload, headers=headers)

    return response.status_code in [200, 201]

# ---- INTERFAZ DE STREAMLIT ----
st.title("Daily Huddle App")

# 🚀 Descargar `users.csv` actualizado antes de mostrar la interfaz
st.session_state["usuarios_df"] = obtener_usuarios()

# Menú de opciones
menu = st.sidebar.radio("Navegación", ["Registro", "Iniciar Sesión"])

# 🚀 **PANTALLA 1: REGISTRO**
if menu == "Registro":
    st.subheader("Registro de Usuario")

    usuario_nuevo = st.text_input("Usuario").strip()
    password_nuevo = st.text_input("Contraseña", type="password")
    boton_registro = st.button("Registrar")

    if boton_registro:
        if usuario_nuevo and password_nuevo:
            if guardar_usuario(usuario_nuevo, password_nuevo):
                st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
                st.session_state["usuarios_df"] = obtener_usuarios()  # 🚀 Actualiza la lista en tiempo real
            else:
                st.error(f"El usuario '{usuario_nuevo}' ya existe en el sistema.")
        else:
            st.error("Debes ingresar un usuario y contraseña.")

# 🚀 **PANTALLA 2: INICIAR SESIÓN**
if menu == "Iniciar Sesión":
    st.subheader("Inicio de Sesión")

    usuario = st.text_input("Usuario").strip().lower()
    password = st.text_input("Contraseña", type="password")
    boton_login = st.button("Iniciar Sesión")

    if boton_login:
        usuarios_df = st.session_state["usuarios_df"]

        # 🚀 Convertimos todo a minúsculas para evitar problemas de coincidencia
        usuarios_df["Usuario"] = usuarios_df["Usuario"].astype(str).str.strip().str.lower()

        if ((usuarios_df["Usuario"] == usuario) & (usuarios_df["Contraseña"] == password)).any():
            st.session_state["logged_in"] = True
            st.session_state["usuario"] = usuario
            st.success(f"Bienvenido, {usuario}. Redirigiéndote a tu portal personal...")
        else:
            st.error("Usuario o contraseña incorrectos.")

# 🚀 **PANTALLA 3: PORTAL PERSONAL**
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader(f"Bienvenido a tu portal personal, {st.session_state['usuario']}")
    st.write("Aquí puedes ver tu información y opciones personalizadas.")

    if st.button("Cerrar Sesión"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()
