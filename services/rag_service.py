import numpy as np
import json
import google.generativeai as genai # <-- Importar la biblioteca de Google
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config.settings import EMBEDDINGS_DIR, EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, LLM_MODEL_NAME, TOP_K_CHUNKS

class RAGService:
    def __init__(self):
        print("🔄 Inicializando el servicio RAG con Google Gemini...")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # Configurar la API de Gemini
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.gemini_model = genai.GenerativeModel(LLM_MODEL_NAME)
        else:
            self.gemini_model = None
            print("⚠️ ADVERTENCIA: La clave de API de Google (GOOGLE_API_KEY) no está configurada.")
        
        self.embeddings = None
        self.chunks_metadata = None
        
        self._load_index()

    def _load_index(self):
        """Carga los embeddings y metadatos desde el disco."""
        try:
            self.embeddings = np.load(EMBEDDINGS_DIR / "embeddings.npy")
            with open(EMBEDDINGS_DIR / "chunks_metadata.json", "r", encoding="utf-8") as f:
                self.chunks_metadata = json.load(f)
            print(f"✅ Índice cargado correctamente con {len(self.chunks_metadata)} chunks.")
        except FileNotFoundError:
            print("❌ Error: No se encontraron los archivos del índice de embeddings.")
            print("   Por favor, ejecuta el proceso de 'reindexación' primero.")
            self.embeddings = None
            self.chunks_metadata = None

    def query(self, question: str) -> dict:
        """Realiza una consulta RAG completa."""
        if not self.gemini_model:
            return {"error": "La clave de Google API no está configurada."}
        if self.embeddings is None:
            return {"error": "El índice de conocimiento no está disponible. Ejecuta /api/reindex."}

        # 1. Embedding de la pregunta del usuario
        question_embedding = self.model.encode([question])

        # 2. Búsqueda de similitud del coseno
        similarities = cosine_similarity(question_embedding, self.embeddings)[0]
        
        # 3. Obtener los top-k chunks más relevantes
        top_k_indices = np.argsort(similarities)[::-1][:TOP_K_CHUNKS]
        
        retrieved_chunks = []
        sources = set()
        for idx in top_k_indices:
            chunk_data = self.chunks_metadata[idx]
            retrieved_chunks.append(chunk_data["text"])
            sources.add(chunk_data["metadata"]["source"])

        # 4. Construcción del contexto para el LLM
        context = "\n\n---\n\n".join(retrieved_chunks)
        
        # 5. Generación de la respuesta con el LLM de Gemini
        system_prompt = (
            "Eres un asistente experto en trámites administrativos para familias con miembros con autismo en Andalucía. "
            "Tu tarea es responder a la pregunta del usuario basándote ÚNICAMENTE en el contexto proporcionado. "
            "Si la respuesta no está en el contexto, indica amablemente que no tienes esa información específica. "
            "Responde de forma clara, concisa y en un lenguaje sencillo para las familias. "
            "Al final de tu respuesta, lista las fuentes (documentos) utilizadas."
        )
        
        user_prompt = f"""
        Pregunta: {question}
        
        Contexto relevante:
        ---
        {context}
        ---
        """

        try:
            # Gemini usa un solo mensaje combinando el system prompt y el user prompt
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.gemini_model.generate_content(full_prompt)
            
            answer = response.text
            
            return {
                "respuesta": answer,
                "fuentes": list(sources)
            }

        except Exception as e:
            return {"error": f"Error al contactar con el modelo de lenguaje Gemini: {e}"}
