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

    # 🔥 Intentar Inicializar Firebase y Conectar a Firestore
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)

    # 🔥 Conectar a Firestore
    db = firestore.client()
    st.success("✅ Firebase se ha inicializado correctamente.")

except Exception as e:
    st.error(f"❌ ERROR AL INICIALIZAR FIREBASE: {str(e)}")
    raise
