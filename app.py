import streamlit as st
from firebase_config import registrar_usuario, verificar_usuario

# Configuración de la página
st.set_page_config(page_title="Daily Huddle", page_icon="⚡", layout="centered")

# Selección de pestañas
menu = st.sidebar.selectbox("Selecciona una opción", ["Iniciar Sesión", "Registrarse"])

if menu == "Registrarse":
    st.title("📝 Registro de Usuario")

    nombre = st.text_input("Nombre")
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Registrarse"):
        if nombre and email and password:
            success, message = registrar_usuario(email, password, nombre)
            st.success(message) if success else st.error(message)
        else:
            st.error("❌ Todos los campos son obligatorios.")

elif menu == "Iniciar Sesión":
    st.title("🔐 Iniciar Sesión")

    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        success, user_id = verificar_usuario(email, password)
        if success:
            st.success(f"✅ Bienvenido {email}!")
            st.session_state["user_id"] = user_id  # Guardar sesión
        else:
            st.error(user_id)
