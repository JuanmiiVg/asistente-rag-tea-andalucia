from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import time

# Servicios propios
from services.perfil_service import agregar_conversacion
from services.process_pdfs import run_pdf_processing
from services.chunking import run_chunking
from services.embeddings import run_embedding_generation
from services.rag_service import RAGService
from services.agent_service import SimpleAgent
from services.logger_service import log_interaction, log_error

def cargar_historial(usuario_id: str):
    ruta = f"data/perfiles/{usuario_id}.json"

    if not os.path.exists(ruta):
        return {"conversaciones": []}

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return {"conversaciones": []}
            return json.loads(data)
    except:
        return {"conversaciones": []}

# --- Modelos de Pydantic para la API ---
class QueryRequest(BaseModel):
    pregunta: str
    usuario_id: str = "usuario_juan"  # <-- opcional: puedes pasarlo desde el frontend


class Source(BaseModel):
    documento: str


class QueryResponse(BaseModel):
    respuesta: str
    fuentes: List[Source]


class HealthResponse(BaseModel):
    status: str
    vector_store: str


class AgentRequest(BaseModel):
    instruccion: str
    usuario_id: str = "usuario_juan"


# --- Inicialización ---
app = FastAPI(
    title="Asistente RAG para TEA Andalucía",
    description="API para consultar información sobre trámites para familias con miembros con autismo en Andalucía."
)

# Instancia del servicio RAG
rag_service_instance: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Inicializa el servicio RAG solo la primera vez."""
    global rag_service_instance
    if rag_service_instance is None:
        rag_service_instance = RAGService()
    return rag_service_instance


# --- Archivos estáticos ---
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse('static/index.html')


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    service = get_rag_service()
    vector_store_status = "connected" if service.embeddings is not None else "disconnected"
    return {"status": "ok", "vector_store": vector_store_status}


@app.post("/api/reindex")
async def reindex_data():
    """Reconstruye embeddings, chunks e índice."""
    global rag_service_instance
    try:
        run_pdf_processing()
        run_chunking()
        run_embedding_generation()

        # Reiniciar el servicio tras regenerar índice
        rag_service_instance = RAGService()

        return {"message": "Índice reconstruido exitosamente."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la reindexación: {str(e)}")


@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Endpoint principal: consulta el sistema RAG con la pregunta del usuario.
    Aquí también se guardan las conversaciones en JSON y se registra en logs.
    """
    inicio = time.time()
    service = get_rag_service()

    if service.embeddings is None:
        log_error("/api/query", request.usuario_id, "Índice no disponible", "IndexError")
        raise HTTPException(status_code=503, 
                            detail="El índice no está disponible. Ejecuta /api/reindex primero.")

    # --- Procesar la pregunta con el modelo ---
    result = service.query(request.pregunta)

    if "error" in result:
        log_error("/api/query", request.usuario_id, result["error"], "QueryError")
        raise HTTPException(status_code=500, detail=result["error"])

    respuesta = result["respuesta"]
    usuario_id = request.usuario_id
    latencia_ms = (time.time() - inicio) * 1000

    # --- Guardar conversación en JSON ---
    agregar_conversacion(usuario_id, request.pregunta, respuesta)

    # --- Registrar en logs ---
    log_interaction(
        endpoint="/api/query",
        usuario_id=usuario_id,
        entrada=request.pregunta,
        salida=respuesta,
        latencia_ms=latencia_ms,
        fuentes=result.get("fuentes", []),
        metadata={"model": "gemini-2.5-flash-lite"}
    )

    # --- Crear objetos Pydantic para la respuesta ---
    fuentes_formateadas = [Source(documento=doc) for doc in result["fuentes"]]

    return QueryResponse(respuesta=respuesta, fuentes=fuentes_formateadas)

@app.get("/api/historial")
async def obtener_historial(usuario_id: str = "usuario_juan"):
    """
    Devuelve el historial guardado del usuario.
    Se llama desde el frontend cuando recarga la página.
    """
    perfil = cargar_historial(usuario_id)
    return perfil


@app.post("/api/agent")
async def run_agent(request: AgentRequest):
    """Ejecuta el agente simple: puede responder o crear una 'solicitud' en disco."""
    inicio = time.time()
    try:
        service = get_rag_service()
        agent = SimpleAgent(rag_service=service)
        result = agent.perform_task(request.instruccion, request.usuario_id)

        if result.get("status") == "error":
            latencia_ms = (time.time() - inicio) * 1000
            log_error("/api/agent", request.usuario_id, result.get("detail"), "AgentError")
            raise HTTPException(status_code=500, detail=result.get("detail"))

        latencia_ms = (time.time() - inicio) * 1000
        accion = result.get("action", "unknown")

        # --- Registrar en logs ---
        log_interaction(
            endpoint="/api/agent",
            usuario_id=request.usuario_id,
            entrada=request.instruccion,
            salida=result.get("respuesta", result.get("path", ""))[:500],
            latencia_ms=latencia_ms,
            fuentes=result.get("fuentes", []),
            metadata={"action_type": accion},
            accion_agente=accion
        )

        return result

    except Exception as e:
        latencia_ms = (time.time() - inicio) * 1000
        log_error("/api/agent", request.usuario_id, str(e), "ExceptionError")
        raise HTTPException(status_code=500, detail=str(e))