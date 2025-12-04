# Cómo usar el servidor Flask para visualizar diagramas

## Paso 1: Instalar Flask (si no lo has hecho ya)
```powershell
pip install flask
```

## Paso 2: Ejecutar el servidor Flask
Desde la carpeta `rag_teandalucia`:
```powershell
cd C:\Users\juanm\Documents\BigData\rag_Proyecto\rag_teandalucia
python .\scripts\serve_diagram.py
```

Deberías ver en la terminal:
```
============================================================
🚀 Servidor Flask iniciado para visualizar el diagrama
============================================================
📊 Abre tu navegador en: http://127.0.0.1:5001
============================================================
```

## Paso 3: Abrir en el navegador
Abre tu navegador y ve a:
```
http://127.0.0.1:5001
```

## ¿Qué verás?
Una página HTML con:
- **Diagrama de flujo Mermaid** — muestra cómo fluyen las solicitudes (RAG + agente)
- **Detalles técnicos** — LLM, embeddings, parámetros, endpoints
- **Pipeline de datos** — proceso desde PDFs hasta búsqueda vectorial
- **Instrucciones de ejecución** — pasos para usar la API
- **Información sobre PLN** — por qué es útil en este proyecto

## Parar el servidor
Presiona `CTRL+C` en la terminal donde ejecutaste `serve_diagram.py`.

## Notas
- El servidor está en modo **debug** (recarga automáticamente si cambias el código).
- Es un servidor de **desarrollo**, no apto para producción.
- El diagrama se renderiza con **Mermaid.js** (requiere conexión a internet para cargar la librería).

---

**Alternativa:** Si Flask no funciona bien, puedes abrir el archivo `DOCUMENTACION.md` directamente en cualquier editor Markdown online que soporte Mermaid (ej: GitHub, Notion, etc.).
