from pathlib import Path
import json
from datetime import datetime
from typing import Optional

from .rag_service import RAGService
from config.settings import DATA_DIR


class SimpleAgent:
    """Un agente muy sencillo que puede: 1) consultar el RAG para obtener información
    y 2) crear una 'solicitud' (archivo JSON) basada en la información recuperada.

    Este agente usa heurísticas simples para decidir si debe 'actuar' (crear un archivo)
    o sólo responder con información.
    """

    def __init__(self, rag_service: Optional[RAGService] = None):
        self.rag = rag_service or RAGService()

        # Carpeta donde el agente guardará acciones/solicitudes
        self.solicitudes_dir = DATA_DIR / "solicitudes"
        self.solicitudes_dir.mkdir(parents=True, exist_ok=True)

    def perform_task(self, instruction: str, usuario_id: str = "anonimo") -> dict:
        """Interpreta la instrucción y actúa.

        Reglas sencillas:
        - Si la instrucción contiene 'crear' o 'generar' + 'solicitud'|'documento' =>
          hace RAG + crea un JSON en `data/solicitudes/`
        - En otro caso, devuelve la respuesta RAG al usuario.
        """

        text = instruction.lower()
        should_create = any(k in text for k in ["crear solicitud", "generar solicitud", "crear documento", "generar documento", "crear solicitud", "crear solicitud de"]) or (
            ("crear" in text or "generar" in text) and ("solicitud" in text or "documento" in text)
        )

        # Obtener contexto/respuesta desde el RAG
        rag_result = self.rag.query(instruction)

        if "error" in rag_result:
            return {"status": "error", "detail": rag_result.get("error")}

        respuesta = rag_result.get("respuesta", "")

        if should_create:
            # Crear un archivo JSON con la 'solicitud' que contenga la instrucción, la respuesta RAG y metadatos
            timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            filename = f"solicitud_{usuario_id}_{timestamp}.json"
            path = self.solicitudes_dir / filename

            contenido = {
                "usuario_id": usuario_id,
                "instruccion": instruction,
                "respuesta": respuesta,
                "fuentes": rag_result.get("fuentes", []),
                "creado_en": timestamp,
            }

            with open(path, "w", encoding="utf-8") as f:
                json.dump(contenido, f, ensure_ascii=False, indent=2)

            return {"status": "ok", "action": "created_solicitud", "path": str(path), "contenido": contenido}

        # Si no hay acción, simplemente devolver la respuesta RAG
        return {"status": "ok", "action": "answer_only", "respuesta": respuesta, "fuentes": rag_result.get("fuentes", [])}


if __name__ == '__main__':
    agent = SimpleAgent()
    print(agent.perform_task("¿Cuáles son los pasos para solicitar el reconocimiento de discapacidad y crea una solicitud de ejemplo", "usuario_demo"))
