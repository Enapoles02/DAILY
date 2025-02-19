import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st
import json

# Cargar las credenciales desde Streamlit Secrets
if "FIREBASE_CREDENTIALS" not in st.secrets:
    raise ValueError("❌ ERROR: FIREBASE_CREDENTIALS no está configurado en Streamlit Secrets.")

firebase_dict = json.loads(json.dumps(st.secrets["FIREBASE_CREDENTIALS"]))  # Convertir JSON a diccionario

# Inicializar Firebase si aún no está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Conectar con Firestore

# Función para registrar un usuario en Firebase Authentication
def registrar_usuario(email, password, nombre):
    try:
        user = auth.create_user(email=email, password=password)
        user_data = {
            "uid": user.uid,
            "email": email,
            "nombre": nombre
        }
        db.collection("users").document(user.uid).set(user_data)  # Guardar en Firestore
        return True, "✅ Usuario registrado con éxito."
    except Exception as e:
        return False, f"❌ Error al registrar usuario: {str(e)}"

# Función para verificar credenciales de usuario
def verificar_usuario(email, password):
    try:
        user_record = auth.get_user_by_email(email)
        return True, user_record.uid
    except Exception as e:
        return False, f"❌ Error de autenticación:

