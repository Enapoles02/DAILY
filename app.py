import streamlit as st
import pandas as pd
import os

# Ruta del archivo CSV en el repositorio de GitHub
DB_FILE = "users.csv"

# Título del portal
st.title("Registro de Usuarios")

# Formulario de registro
with st.form("register_form"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    area = st.selectbox("Área", ["Finanzas", "TI", "Recursos Humanos", "Ventas", "Otro"])
    password = st.text_input("Contraseña", type="password")
    submit_button = st.form_submit_button("Registrar")

# Función para guardar usuario en CSV
def guardar_usuario(nombre, correo, area, password):
    df = pd.DataFrame([[nombre, correo, area, password]], 
                      columns=["Nombre", "Correo", "Área", "Contraseña"])
    
    if os.path.exists(DB_FILE):
        df_existente = pd.read_csv(DB_FILE)
        df = pd.concat([df_existente, df], ignore_index=True)
    
    df.to_csv(DB_FILE, index=False)

# Procesar registro
if submit_button:
    if nombre and correo and area and password:
        guardar_usuario(nombre, correo, area, password)
        st.success(f"Usuario {nombre} registrado exitosamente")
    else:
        st.error("Todos los campos son obligatorios")

# Mostrar usuarios registrados (solo para admins)
if st.checkbox("Mostrar usuarios registrados"):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.dataframe(df)
    else:
        st.error("No hay usuarios registrados aún.")
