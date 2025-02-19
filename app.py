import streamlit as st
import pandas as pd
import os

# Archivo CSV donde se guardarán los usuarios
DB_FILE = "users.csv"

# Verifica si el CSV existe, si no, lo crea con columnas predeterminadas
if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["Usuario", "Contraseña"])
    df_init.to_csv(DB_FILE, index=False)

# Función para verificar usuario
def verificar_usuario(usuario, password):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if ((df["Usuario"] == usuario) & (df["Contraseña"] == password)).any():
            return True
    return False

# Función para registrar un nuevo usuario
def registrar_usuario(usuario, password):
    df = pd.read_csv(DB_FILE)
    if usuario in df["Usuario"].values:
        return False  # Usuario ya registrado
    nuevo_usuario = pd.DataFrame([[usuario, password]], columns=["Usuario", "Contraseña"])
    df = pd.concat([df, nuevo_usuario], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return True

# ---- INTERFAZ DE STREAMLIT ----

st.title("Daily Huddle App")

# 1️⃣ PANTALLA DE REGISTRO/LOGIN
st.subheader("Registro / Inicio de Sesión")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")
boton_login = st.button("Iniciar Sesión")

if boton_login:
    if verificar_usuario(usuario, password):
        st.session_state["logged_in"] = True
        st.session_state["usuario"] = usuario
        st.success("Inicio de sesión exitoso. Accediendo a la app...")
    else:
        st.error("Usuario o contraseña incorrectos. Regístrate si aún no tienes cuenta.")

st.subheader("¿Nuevo aquí?")
usuario_nuevo = st.text_input("Nuevo Usuario")
password_nuevo = st.text_input("Nueva Contraseña", type="password")
boton_registro = st.button("Registrar")

if boton_registro:
    if usuario_nuevo and password_nuevo:
        if registrar_usuario(usuario_nuevo, password_nuevo):
            st.success("Usuario registrado con éxito. Ahora inicia sesión.")
        else:
            st.error("El usuario ya existe. Intenta con otro nombre.")
    else:
        st.error("Debes ingresar un usuario y contraseña.")

# 2️⃣ VERIFICAR SI EL USUARIO ESTÁ LOGUEADO PARA MOSTRAR LAS PESTAÑAS
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    
    # 3️⃣ NAVEGACIÓN ENTRE PESTAÑAS
    menu = st.sidebar.radio("Navegación", ["Overview", "Top 3", "Action Board", "Communications", "Calendar"])

    # 4️⃣ CONTENIDO DE CADA PESTAÑA
    if menu == "Overview":
        st.subheader("Bienvenido a Daily Huddle")
        st.write("Aquí puedes gestionar tus prioridades diarias de manera estructurada.")
        st.write("Si necesitas ayuda, contacta a: **enrique.napoles@dbschenker.com**")

    elif menu == "Top 3":
        st.subheader("Tus 3 prioridades del día")
        prioridad1 = st.text_input("Prioridad 1")
        prioridad2 = st.text_input("Prioridad 2")
        prioridad3 = st.text_input("Prioridad 3")
        if st.button("Guardar Prioridades"):
            st.success("¡Tus prioridades han sido guardadas!")

    elif menu == "Action Board":
        st.subheader("Acciones y Seguimiento")
        accion = st.text_area("Registra aquí las acciones a tomar")
        if st.button("Guardar Acción"):
            st.success("Acción registrada con éxito.")

    elif menu == "Communications":
        st.subheader("Comunicaciones y Mensajes")
        st.write("Aquí se mostrarán las comunicaciones importantes.")

    elif menu == "Calendar":
        st.subheader("Calendario de Eventos")
        st.write("Aquí puedes ver los eventos importantes y recordatorios.")

