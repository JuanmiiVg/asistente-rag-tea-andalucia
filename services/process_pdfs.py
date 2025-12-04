import os
from pypdf import PdfReader
from pathlib import Path  # <-- ¡AÑADE ESTA LÍNEA!
from config.settings import DATA_DIR, DATA_CLEAN_DIR

def clean_text(text: str) -> str:
    """Limpia el texto extraído del PDF."""
    # Eliminar espacios en blanco múltiples y saltos de línea innecesarios
    text = ' '.join(text.split())
    return text.strip()

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrae y limpia el texto de un único archivo PDF."""
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
        return clean_text(full_text)
    except Exception as e:
        print(f"❌ Error al leer {pdf_path.name}: {e}")
        return ""

def run_pdf_processing():
    """Función principal para procesar todos los PDFs en la carpeta 'data'."""
    print("🚀 Iniciando procesamiento de PDFs...")
    pdf_files = [f for f in DATA_DIR.glob("*.pdf")]
    
    if not pdf_files:
        print(f"⚠️ No se encontraron archivos PDF en la carpeta: {DATA_DIR}")
        return

    for pdf_path in pdf_files:
        print(f"📄 Procesando: {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            output_path = DATA_CLEAN_DIR / f"{pdf_path.stem}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Texto limpio guardado en: {output_path}")
        else:
            print(f"⚠️ No se pudo extraer texto de: {pdf_path.name}")

    print("🏁 Procesamiento de PDFs finalizado.")

if __name__ == '__main__':
    run_pdf_processing()