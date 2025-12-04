"""
Logger service para registrar interacciones del chatbot en formato JSON.
Guarda cada consulta RAG y acción del agente en logs/interactions.jsonl
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

# Configurar directorio de logs
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Archivo de interacciones
INTERACTIONS_LOG = LOGS_DIR / "interactions.jsonl"

# Archivo de errores
ERRORS_LOG = LOGS_DIR / "errors.log"

# Configurar logger de Python estándar
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ERRORS_LOG),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_interaction(
    endpoint: str,
    usuario_id: str,
    entrada: str,
    salida: str,
    latencia_ms: float,
    fuentes: Optional[list] = None,
    metadata: Optional[Dict[str, Any]] = None,
    accion_agente: Optional[str] = None
) -> None:
    """
    Registra una interacción (RAG o agente) en logs/interactions.jsonl
    
    Args:
        endpoint: ej. "/api/query" o "/api/agent"
        usuario_id: ID del usuario
        entrada: Pregunta o instrucción
        salida: Respuesta o resultado
        latencia_ms: Tiempo en milisegundos
        fuentes: Lista de fuentes consultadas
        metadata: Datos adicionales (ej. tokens, modelo, etc.)
        accion_agente: Tipo de acción (ej. "created_solicitud", "answer_only")
    """
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoint": endpoint,
        "usuario_id": usuario_id,
        "entrada": entrada[:500],  # Limitar tamaño
        "salida": salida[:500],
        "latencia_ms": round(latencia_ms, 2),
        "fuentes": fuentes or [],
        "accion_agente": accion_agente,
        "metadata": metadata or {}
    }
    
    try:
        with open(INTERACTIONS_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.info(f"[{endpoint}] Usuario: {usuario_id} | Latencia: {latencia_ms:.0f}ms")
    except Exception as e:
        logger.error(f"Error al registrar interacción: {e}")


def log_error(
    endpoint: str,
    usuario_id: str,
    error_message: str,
    error_type: str = "GenericError"
) -> None:
    """
    Registra un error en logs/errors.log
    
    Args:
        endpoint: ej. "/api/query"
        usuario_id: ID del usuario
        error_message: Mensaje de error
        error_type: Tipo de error (ej. "APIError", "ValidationError")
    """
    logger.error(f"[{endpoint}] User: {usuario_id} | Type: {error_type} | Message: {error_message}")


def read_interactions_log(limit: Optional[int] = None) -> list:
    """
    Lee el archivo de interacciones y devuelve lista de registros JSON.
    
    Args:
        limit: Número máximo de registros a leer (None = todos)
    
    Returns:
        Lista de diccionarios con interacciones
    """
    records = []
    if not INTERACTIONS_LOG.exists():
        return records
    
    try:
        with open(INTERACTIONS_LOG, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                try:
                    records.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        logger.error(f"Error al leer logs: {e}")
    
    return records


if __name__ == '__main__':
    # Test
    log_interaction(
        endpoint="/api/query",
        usuario_id="test_user",
        entrada="Test question",
        salida="Test answer",
        latencia_ms=1234.56,
        fuentes=["doc1.pdf"],
        metadata={"model": "gemini-2.5"}
    )
    print(f"✅ Log creado en: {INTERACTIONS_LOG}")
    print(f"Registros: {read_interactions_log()}")
