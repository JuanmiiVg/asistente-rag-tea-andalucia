import os
import json
from datetime import datetime

PERFILES_PATH = "data/perfiles"

def cargar_perfil(usuario_id):
    """
    Carga el perfil del usuario desde JSON.
    Si no existe, lo crea con estructura inicial.
    """
    os.makedirs(PERFILES_PATH, exist_ok=True)
    ruta = os.path.join(PERFILES_PATH, f"{usuario_id}.json")

    if not os.path.exists(ruta):
        perfil = {
            "usuario_id": usuario_id,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conversaciones": []
        }
        guardar_perfil(usuario_id, perfil)
    else:
        with open(ruta, "r", encoding="utf-8") as f:
            perfil = json.load(f)

    return perfil


def guardar_perfil(usuario_id, perfil):
    """
    Guarda el perfil del usuario en su archivo JSON.
    """
    ruta = os.path.join(PERFILES_PATH, f"{usuario_id}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=4, ensure_ascii=False)


def agregar_conversacion(usuario_id, mensaje_usuario, respuesta_agente):
    """
    Agrega un turno de conversación al perfil del usuario.
    """
    perfil = cargar_perfil(usuario_id)

    perfil["conversaciones"].append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": mensaje_usuario,
        "agente": respuesta_agente
    })

    guardar_perfil(usuario_id, perfil)
