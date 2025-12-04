# services/chunking.py

# IMPORTACIÓN CORREGIDA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import DATA_CLEAN_DIR, CHUNKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
import json

def run_chunking():
    """Divide los textos limpios en chunks y los guarda."""
    print("🧩 Iniciando el proceso de 'chunking'...")
    
    text_files = [f for f in DATA_CLEAN_DIR.glob("*.txt")]
    if not text_files:
        print(f"⚠️ No se encontraron archivos de texto limpio en: {DATA_CLEAN_DIR}")
        return

    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""] # Separadores lógicos
    )

    for text_path in text_files:
        print(f"📖 Troceando: {text_path.name}")
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        source_chunks = splitter.create_documents([text])
        
        for i, chunk in enumerate(source_chunks):
            all_chunks.append({
                "text": chunk.page_content,
                "metadata": {
                    "source": text_path.name,
                    "chunk_id": i
                }
            })
    
    # Guardar todos los chunks en un único archivo JSON
    output_path = CHUNKS_DIR / "chunks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Se han guardado {len(all_chunks)} chunks en: {output_path}")
    print("🏁 Proceso de 'chunking' finalizado.")

if __name__ == '__main__':
    run_chunking()