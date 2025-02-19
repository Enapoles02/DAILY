import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# 🔥 Verificar que Streamlit cargó las credenciales correctamente
if "FIREBASE_CREDENTIALS" not in st.secrets:
    raise ValueError("❌ ERROR: `FIREBASE_CREDENTIALS` no está disponible en Streamlit.")

try:
    # 🔥 Leer credenciales desde `st.secrets`
    firebase_dict = dict(st.secrets["FIREBASE_CREDENTIALS"])
    firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")

    # 🔥 Inicializar Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)

    # 🔥 Conectar a Firestore
    db = firestore.client()

except Exception as e:
    raise ValueError(f"❌ ERROR AL INICIALIZAR FIREBASE: {str(e)}")

# Función para registrar un usuario en Firestore
def registrar_usuario(usuario, password):
    try:
        doc_ref = db.collection("usuarios").document(usuario.lower())
        if doc_ref.get().exists:
            return False  # El usuario ya existe
        doc_ref.set({"password": password})
        return True
    except Exception as e:
        raise ValueError(f"❌ ERROR REGISTRANDO USUARIO: {str(e)}")

# Función para verificar un usuario en Firestore
def verificar_usuario(usuario, password):
    try:
        doc_ref = db.collection("usuarios").document(usuario.lower())
        doc = doc_ref.get()
        if doc.exists and doc.to_dict().get("password") == password:
            return True
        return False
    except Exception as e:
        raise ValueError(f"❌ ERROR VERIFICANDO USUARIO: {str(e)}")
