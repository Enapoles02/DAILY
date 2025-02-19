import streamlit as st

# 🔍 Verificar si Streamlit detecta las credenciales
if "FIREBASE_CREDENTIALS" not in st.secrets:
    st.error("❌ ERROR: `FIREBASE_CREDENTIALS` no está disponible en Streamlit.")
else:
    st.success("✅ FIREBASE_CREDENTIALS fue cargado correctamente en Streamlit.")
    st.write(st.secrets["FIREBASE_CREDENTIALS"])
