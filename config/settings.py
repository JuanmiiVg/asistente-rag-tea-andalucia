# config/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Construimos la ruta exacta al archivo .env
dotenv_path = BASE_DIR / ".env"

# Cargamos las variables de entorno desde esa ruta explícita
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    print(f"✅ Archivo .env encontrado y cargado desde: {dotenv_path}")
else:
    print(f"❌ ERROR: Archivo .env NO encontrado en la ruta esperada: {dotenv_path}")

api_key_value = os.getenv("GOOGLE_API_KEY")
if api_key_value:
    print(f"🔍 Depuración: La variable GOOGLE_API_KEY se ha cargado correctamente.")
else:
    print(f"🔍 Depuración: La variable GOOGLE_API_KEY es None. Revisa el archivo .env")


# --- Rutas del Proyecto ---
DATA_DIR = BASE_DIR / "data"
DATA_CLEAN_DIR = BASE_DIR / "data_clean"
CHUNKS_DIR = BASE_DIR / "chunks"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"

# --- Configuración de Modelos y APIs ---
# Modelo de embeddings de Hugging Face (multilingüe y ligero)
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Configuración de la API de Google Gemini
# Leemos la variable de entorno por su NOMBRE
GOOGLE_API_KEY = api_key_value
LLM_MODEL_NAME = "models/gemini-2.5-flash-lite" # o "gemini-1.5-pro" para más calidad

# --- Configuración de Chunking ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- Configuración de Búsqueda (RAG) ---
TOP_K_CHUNKS = 4 # Número de fragmentos más relevantes a recuperar

# --- Creación de Directorios ---
# Asegurarse de que los directorios existan antes de empezar
for dir_path in [DATA_DIR, DATA_CLEAN_DIR, CHUNKS_DIR, EMBEDDINGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

print("✅ Configuración cargada y directorios verificados.")