from sentence_transformers import SentenceTransformer
import numpy as np
import json
from config.settings import CHUNKS_DIR, EMBEDDINGS_DIR, EMBEDDING_MODEL_NAME

def run_embedding_generation():
    """Genera y guarda los embeddings para los chunks."""
    print(f"🧠 Iniciando generación de embeddings con el modelo: {EMBEDDING_MODEL_NAME}")
    
    chunks_path = CHUNKS_DIR / "chunks.json"
    if not chunks_path.exists():
        print(f"❌ Error: No se encontró el archivo de chunks en: {chunks_path}")
        print("   Por favor, ejecuta primero el proceso de 'chunking'.")
        return

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks_data = json.load(f)

    texts_to_embed = [chunk["text"] for chunk in chunks_data]
    
    print(f"📊 Generando embeddings para {len(texts_to_embed)} fragmentos de texto...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    
    # Guardar embeddings y chunks
    np.save(EMBEDDINGS_DIR / "embeddings.npy", embeddings)
    with open(EMBEDDINGS_DIR / "chunks_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Embeddings guardados en: {EMBEDDINGS_DIR / 'embeddings.npy'}")
    print(f"✅ Metadatos de chunks guardados en: {EMBEDDINGS_DIR / 'chunks_metadata.json'}")
    print("🏁 Generación de embeddings finalizada.")

if __name__ == '__main__':
    run_embedding_generation()