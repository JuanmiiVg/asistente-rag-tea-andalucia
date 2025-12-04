import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Cargar la API key desde el .env como lo hacemos en el resto del proyecto
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
else:
    print(f"✅ Usando la API Key para listar los modelos disponibles...")
    try:
        genai.configure(api_key=api_key)
        
        # Llamar a la función para listar todos los modelos disponibles
        models = genai.list_models()
        
        print("\n--- Modelos Disponibles para tu API Key ---")
        found_gemini = False
        for model in models:
            # Filtramos para mostrar solo los modelos que soportan 'generateContent'
            if 'generateContent' in model.supported_generation_methods:
                print(f"- Nombre: {model.name} (Display Name: {model.display_name})")
                if "gemini" in model.name.lower():
                    found_gemini = True
        
        if not found_gemini:
            print("\n⚠️ ADVERTENCIA: No se encontró ningún modelo 'gemini' que soporte 'generateContent'.")
            print("   Revisa tu configuración en Google AI Studio (https://makersuite.google.com/app/apikey).")

    except Exception as e:
        print(f"\n❌ ERROR al contactar con la API de Google: {e}")
