import pandas as pd
import requests
import os
import base64

# Configuración de GitHub
GITHUB_REPO = "Enapoles02/DAILY"
GITHUB_TOKEN = os.getenv("TOKEN_DAILY")  # Secreto en GitHub
CSV_FILE = "users.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE}"

# Función para obtener el archivo CSV actualizado desde GitHub
def obtener_usuarios():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code == 200:
        content = response.json()
        csv_data = base64.b64decode(content["content"]).decode("utf-8")
        return pd.read_csv(pd.io.common.StringIO(csv_data))

    return pd.DataFrame(columns=["Usuario", "Contraseña"])  # Si no hay archivo, devuelve un CSV vacío

# Generar un CSV inicial si es necesario
df = obtener_usuarios()
df.to_csv(CSV_FILE, index=False)

# Obtener el SHA del archivo (para actualizarlo en GitHub)
response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
sha = response.json().get("sha", "")

# Subir archivo a GitHub
with open(CSV_FILE, "rb") as f:
    content_encoded = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "message": "Actualizar users.csv automáticamente",
    "content": content_encoded,
    "branch": "main",
    "sha": sha
}

headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.put(GITHUB_API_URL, json=payload, headers=headers)

if response.status_code in [200, 201]:
    print("✅ Archivo CSV actualizado correctamente en GitHub")
else:
    print(f"❌ Error al subir archivo: {response.json()}")
