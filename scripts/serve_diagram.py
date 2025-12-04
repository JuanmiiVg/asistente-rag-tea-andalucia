"""
Script Flask para visualizar el diagrama conversacional del proyecto.
Ejecutar: python scripts/serve_diagram.py
Visitar: http://127.0.0.1:5001
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template con Mermaid embebido
HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asistente TEA - Diagrama Arquitectónico</title>
    <script src="https://unpkg.com/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #667eea;
            font-size: 1.8rem;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .section p {
            color: #555;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        
        .diagram-container {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .mermaid {
            display: flex;
            justify-content: center;
        }
        
        .tech-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .tech-card {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
        }
        
        .tech-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }
        
        .tech-card p {
            font-size: 0.95rem;
            color: #666;
        }
        
        .tech-card code {
            background: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #999;
            border-top: 1px solid #ddd;
        }
        
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        .highlight {
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            margin: 15px 0;
        }
        
        .highlight strong {
            color: #856404;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .tech-details {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Asistente RAG para TEA Andalucía</h1>
            <p>Diagrama Arquitectónico e Información Técnica</p>
        </div>
        
        <div class="content">
            <!-- Diagrama de Flujo -->
            <div class="section">
                <h2>📊 Diagrama Conversacional (Flujo de Interacción)</h2>
                <p>El siguiente diagrama muestra cómo fluye una solicitud desde el usuario hasta la generación de respuesta y posible acción autónoma:</p>
                
                <div class="diagram-container">
                    <div class="mermaid">
                        sequenceDiagram
                            participant Usuario
                            participant Frontend
                            participant API
                            participant RAG as "Retriever (VectorStore)"
                            participant LLM as "Google Gemini"
                            participant Agente as "SimpleAgent"
                            participant Disk as "data/solicitudes/"

                            Usuario->>Frontend: 🗣️ Pregunta / Instrucción
                            Frontend->>API: POST /api/query o /api/agent
                            
                            alt Consulta RAG Normal
                                API->>RAG: Buscar top-k fragmentos similares
                                RAG-->>API: Documentos relevantes
                                API->>LLM: Prompt (system + contexto)
                                LLM-->>API: Respuesta en lenguaje natural
                                API-->>Frontend: ✅ Mostrar respuesta + fuentes
                                Frontend-->>Usuario: Visualizar resultado
                            else Acción del Agente
                                API->>Agente: perform_task(instrucción)
                                Agente->>RAG: Consulta RAG para contexto
                                RAG-->>Agente: Fragmentos relevantes
                                Agente->>LLM: Generar contenido de solicitud
                                LLM-->>Agente: Respuesta generada
                                Agente->>Disk: 💾 Crear JSON con solicitud
                                Agente-->>API: ✅ Resultado (path + contenido)
                                API-->>Frontend: Confirmar creación
                                Frontend-->>Usuario: Mostrar ubicación del archivo
                            end
                    </div>
                </div>
            </div>
            
            <!-- Detalles Técnicos -->
            <div class="section">
                <h2>🔧 Detalles Técnicos</h2>
                <p>Resumen de la stack tecnológica y configuración utilizada en el proyecto:</p>
                
                <div class="tech-details">
                    <div class="tech-card">
                        <h3>📝 LLM (Modelo de Lenguaje)</h3>
                        <p><strong>Proveedor:</strong> Google Gemini</p>
                        <p><code>gemini-2.5-flash-lite</code></p>
                        <p>Modelo ligero optimizado para respuestas rápidas con suficiente capacidad para entender contexto y generar respuestas coherentes.</p>
                    </div>
                    
                    <div class="tech-card">
                        <h3>🧠 Embeddings</h3>
                        <p><strong>Modelo:</strong> Sentence-Transformers</p>
                        <p><code>paraphrase-multilingual-MiniLM-L12-v2</code></p>
                        <p>Embeddings multilingües compactos para representar texto en espacios semánticos y búsqueda por similitud.</p>
                    </div>
                    
                    <div class="tech-card">
                        <h3>🗄️ Vectorstore</h3>
                        <p><strong>Almacenamiento:</strong> Local (NumPy)</p>
                        <p><code>embeddings.npy</code> + <code>chunks_metadata.json</code></p>
                        <p>Implementación local con búsqueda por cosine similarity. Escalable a Chroma/FAISS en futuro.</p>
                    </div>
                    
                    <div class="tech-card">
                        <h3>⚙️ Parámetros RAG</h3>
                        <p><strong>Chunk Size:</strong> 1000 caracteres</p>
                        <p><strong>Overlap:</strong> 200 caracteres</p>
                        <p><strong>Top-K:</strong> 4 fragmentos</p>
                        <p>Configuración balanceada para contexto suficiente sin ruido excesivo.</p>
                    </div>
                    
                    <div class="tech-card">
                        <h3>🚀 Framework Web</h3>
                        <p><strong>API:</strong> FastAPI</p>
                        <p><strong>Servidor:</strong> Uvicorn</p>
                        <p><strong>Frontend:</strong> HTML/CSS/JavaScript</p>
                        <p>Stack moderno y performante con documentación automática.</p>
                    </div>
                    
                    <div class="tech-card">
                        <h3>🤖 Agente</h3>
                        <p><strong>Tipo:</strong> SimpleAgent (heurístico)</p>
                        <p><strong>Herramientas:</strong> RAG + Crear archivo</p>
                        <p>Agente sencillo que decide crear solicitudes en <code>data/solicitudes/</code> basándose en palabras clave.</p>
                    </div>
                </div>
            </div>
            
            <!-- Pipeline de Procesamiento -->
            <div class="section">
                <h2>📦 Pipeline de Procesamiento de Datos</h2>
                <p>Flujo desde documentos PDF hasta búsqueda vectorial disponible:</p>
                
                <div class="diagram-container">
                    <div class="mermaid">
                        graph LR
                            A["📄 PDFs en data/"] -->|process_pdfs.py| B["📝 Texto limpio (data_clean/)"]
                            B -->|chunking.py| C["🧩 Chunks JSON (chunks/)"]
                            C -->|embeddings.py| D["🧠 Embeddings NumPy (embeddings/)"]
                            D -->|rag_service.py| E["🔍 Búsqueda + RAG"]
                            E --> F["💬 Respuesta + Fuentes"]
                    </div>
                </div>
            </div>
            
            <!-- Instrucciones de Ejecución -->
            <div class="section">
                <h2>🚀 Instrucciones de Ejecución</h2>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">1. Arrancar el servidor (Terminal A)</h3>
                <div class="highlight">
                    <code>cd C:\Users\juanm\Documents\BigData\rag_Proyecto\rag_teandalucia</code><br>
                    <code>$env:PYTHONPATH = $PWD</code><br>
                    <code>python -m uvicorn main:app --host 127.0.0.1 --port 9000</code>
                </div>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">2. Abrir la UI en el navegador (Terminal A sigue corriendo)</h3>
                <div class="highlight">
                    <code>http://127.0.0.1:9000</code>
                </div>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">3. Ejemplo: Consultar RAG (Terminal B)</h3>
                <div class="highlight">
                    <code>curl -X POST "http://127.0.0.1:9000/api/query" \</code><br>
                    <code>  -H "Content-Type: application/json" \</code><br>
                    <code>  -d '{ "pregunta": "¿Cuáles son los pasos para solicitar reconocimiento de discapacidad?", "usuario_id": "usuario_juan" }'</code>
                </div>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">4. Ejemplo: Usar el Agente (crear solicitud)</h3>
                <div class="highlight">
                    <code>curl -X POST "http://127.0.0.1:9000/api/agent" \</code><br>
                    <code>  -H "Content-Type: application/json" \</code><br>
                    <code>  -d '{ "instruccion": "Generar solicitud de reconocimiento de discapacidad", "usuario_id": "usuario_juan" }'</code>
                </div>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">5. Verificar archivo creado</h3>
                <div class="highlight">
                    <code>dir .\data\solicitudes</code><br>
                    <code>type .\data\solicitudes\solicitud_usuario_juan_*.json</code>
                </div>
            </div>
            
            <!-- Endpoints disponibles -->
            <div class="section">
                <h2>🔌 Endpoints disponibles</h2>
                
                <div class="tech-card">
                    <h3>GET /</h3>
                    <p>Sirve la UI estática (HTML/CSS/JS).</p>
                </div>
                
                <div class="tech-card">
                    <h3>GET /api/health</h3>
                    <p>Verifica el estado del servidor y si el índice está conectado.</p>
                </div>
                
                <div class="tech-card">
                    <h3>POST /api/reindex</h3>
                    <p>Reconstruye embeddings y chunks desde los PDFs en <code>data/</code>.</p>
                </div>
                
                <div class="tech-card">
                    <h3>POST /api/query</h3>
                    <p>Consulta RAG: devuelve respuesta + fuentes.</p>
                    <p><strong>Body:</strong> <code>{ "pregunta": "...", "usuario_id": "..." }</code></p>
                </div>
                
                <div class="tech-card">
                    <h3>POST /api/agent</h3>
                    <p>Ejecuta el agente: puede crear solicitudes en <code>data/solicitudes/</code>.</p>
                    <p><strong>Body:</strong> <code>{ "instruccion": "...", "usuario_id": "..." }</code></p>
                </div>
                
                <div class="tech-card">
                    <h3>GET /api/historial</h3>
                    <p>Obtiene el historial de conversaciones de un usuario.</p>
                    <p><strong>Query:</strong> <code>?usuario_id=usuario_juan</code></p>
                </div>
            </div>
            
            <!-- PLN en el proyecto -->
            <div class="section">
                <h2>🧠 Procesamiento del Lenguaje Natural (PLN)</h2>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">¿Qué es el PLN y por qué es útil aquí?</h3>
                <p><strong>PLN (Natural Language Processing):</strong> Conjunto de técnicas para que las máquinas comprendan, analicen y generen lenguaje humano.</p>
                
                <div class="highlight">
                    <strong>En este proyecto usamos PLN para:</strong><br>
                    ✅ <strong>Extracción de texto:</strong> Limpiar y procesar documentos PDF.<br>
                    ✅ <strong>Vectorización:</strong> Convertir texto a embeddings (representación numérica de significado).<br>
                    ✅ <strong>Búsqueda semántica:</strong> Encontrar fragmentos relevantes basándose en similitud de significado, no palabras clave exactas.<br>
                    ✅ <strong>Generación de lenguaje:</strong> Gemini produce respuestas coherentes en lenguaje natural.<br>
                    ✅ <strong>Accesibilidad:</strong> Adaptamos respuestas complejas a lenguaje sencillo.
                </div>
                
                <h3 style="color: #667eea; margin-top: 15px; margin-bottom: 10px;">Beneficios en este contexto</h3>
                <ul style="margin-left: 20px; line-height: 1.8; color: #666;">
                    <li>📚 <strong>Conocimiento contextual:</strong> Respuestas basadas en documentos reales, reduciendo alucinaciones.</li>
                    <li>🎯 <strong>Precisión:</strong> Búsqueda semántica vs. búsqueda por palabras clave (más flexible y precisa).</li>
                    <li>♿ <strong>Inclusión:</strong> Familias con diferentes niveles educativos pueden entender respuestas complejas.</li>
                    <li>⚡ <strong>Automatización:</strong> Generar borradores de solicitudes sin intervención manual.</li>
                    <li>📊 <strong>Escalabilidad:</strong> Nuevos documentos se añaden al índice sin cambiar el código.</li>
                </ul>
            </div>
            
            <!-- Siguientes mejoras -->
            <div class="section">
                <h2>🔮 Siguientes Mejoras Recomendadas</h2>
                
                <div class="tech-card">
                    <h3>1. Integración completa con LangChain</h3>
                    <p>Usar <code>RetrievalQA</code>, <code>Chroma</code> como vectorstore y <code>langchain.Agent</code> para capacidades más avanzadas.</p>
                </div>
                
                <div class="tech-card">
                    <h3>2. Monitorización</h3>
                    <p>Instrumentar con LangSmith, Langfuse o Helicone para trazar prompts, respuestas y latencias.</p>
                </div>
                
                <div class="tech-card">
                    <h3>3. Seguridad</h3>
                    <p>Eliminar clave del repo, usar <code>.env.example</code>, autenticación en endpoints sensibles.</p>
                </div>
                
                <div class="tech-card">
                    <h3>4. Tests y CI/CD</h3>
                    <p>Tests unitarios e integración, GitHub Actions para validación automática.</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Asistente RAG para TEA Andalucía © 2025 | 
            <a href="https://github.com">GitHub</a> | 
            Documentación: <code>DOCUMENTACION.md</code>
            </p>
        </div>
    </div>
    
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Renderiza la página principal con diagrama Mermaid."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'Diagram server is running'}

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Servidor Flask iniciado para visualizar el diagrama")
    print("="*60)
    print("📊 Abre tu navegador en: http://127.0.0.1:5001")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5001, debug=True)
