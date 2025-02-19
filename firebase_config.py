import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Cargar credenciales desde GitHub Secrets
firebase_json = os.getenv("FIREBASE_CREDENTIALS")
firebase_dict = json.loads(firebase_json)  # Convertir string JSON a diccionario

# Inicializar Firebase con las credenciales
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Función para registrar un usuario en Firestore
def registrar_usuario(usuario, password):
    doc_ref = db.collection("usuarios").document(usuario.lower())
    if doc_ref.get().exists:
        return False  # El usuario ya existe
    doc_ref.set({"password": password})
    return True

# Función para verificar un usuario
def verificar_usuario(usuario, password):
    doc_ref = db.collection("usuarios").document(usuario.lower())
    doc = doc_ref.get()
    if doc.exists and doc.to_dict().get("password") == password:
        return True
    return False
