import pandas as pd
import requests
import os
import base64

# Configuración de GitHub
GITHUB_REPO = "Enapoles02/DAILY"
GITHUB_TOKEN = os.getenv("TOKEN_DAILY")  # Usamos el secreto de GitHub
CSV_FILE = "users.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE}"

# Crear un DataFrame con usuarios de prueba
df = pd.DataFrame([
    {"Usuario": "admin", "Contraseña": "admin123"},
    {"Usuario": "test", "Contraseña": "test123"}
])

# Convertir DataFrame a CSV
csv_data = df.to_csv(index=False)

# Obtener el SHA del archivo (si ya existe)
response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
sha = response.json().get("sha", "")

# Crear payload para subir archivo
payload = {
    "message": "Generar users.csv automáticamente",
    "content": base64.b64encode(csv_data.encode()).decode(),
    "branch": "main",
}
if sha:
    payload["sha"] = sha  # Necesario si el archivo ya existe

# Subir archivo a GitHub
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.put(GITHUB_API_URL, json=payload, headers=headers)

if response.status_code == 201 or response.status_code == 200:
    print("✅ Archivo CSV creado correctamente en GitHub")
else:
    print(f"❌ Error al subir archivo: {response.json()}")
