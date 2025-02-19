import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Cargar credenciales desde GitHub Secrets
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("⚠️ ERROR: La clave FIREBASE_CREDENTIALS no está configurada en GitHub Secrets.")

try:
    firebase_dict = json.loads(firebase_json)  # Convertir string JSON a diccionario
    # 🔥 Reemplazar saltos de línea en la clave privada
    firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")
except json.JSONDecodeError:
    raise ValueError("⚠️ ERROR: FIREBASE_CREDENTIALS no contiene un JSON válido. Verifica que lo pegaste correctamente en GitHub Secrets.")

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
