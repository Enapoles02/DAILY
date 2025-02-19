import streamlit as st
from firebase_config import registrar_usuario, verificar_usuario

st.title("Daily Huddle App")

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
            if registrar_usuario(usuario_nuevo, password_nuevo):
                st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
            else:
                st.error("El usuario ya existe en el sistema.")
        else:
            st.error("Debes ingresar un usuario y contraseña.")

# 🚀 **PANTALLA 2: INICIAR SESIÓN**
if menu == "Iniciar Sesión":
    st.subheader("Inicio de Sesión")

    usuario = st.text_input("Usuario").strip()
    password = st.text_input("Contraseña", type="password")
    boton_login = st.button("Iniciar Sesión")

    if boton_login:
        if verificar_usuario(usuario, password):
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
