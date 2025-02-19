import os

# 🔍 DEPURACIÓN: Ver si `FIREBASE_CREDENTIALS` está disponible en Streamlit
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("❌ ERROR: `FIREBASE_CREDENTIALS` NO está disponible en el entorno de Streamlit.")

print("✅ FIREBASE_CREDENTIALS está disponible en el entorno.")
