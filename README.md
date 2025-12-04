# 🤖 Asistente RAG para TEA Andalucía

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-orange?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)](https://github.com)

> Un chatbot inteligente que combina **Recuperación Aumentada por Generación (RAG)** y **capacidades de agente autónomo** para asistir a trabajadores y familias con información sobre trámites administrativos para personas con autismo en Andalucía.

---

## 📋 Características principales

✅ **RAG (Retrieval-Augmented Generation)**
- Búsqueda vectorial semántica en documentos
- Respuestas contextualizadas basadas en fuentes reales
- Reduce alucinaciones del LLM

✅ **Agente Autónomo Simple**
- Interpreta instrucciones naturales
- Genera documentos/solicitudes automáticamente
- Crea archivos estructurados en JSON

✅ **API REST con FastAPI**
- Endpoints bien documentados
- Modelos Pydantic validados
- Documentación automática en `/docs`

✅ **Interfaz Web Interactiva**
- UI moderna con HTML/CSS/JavaScript
- Historial de conversaciones
- Visualización de fuentes consultadas

✅ **Diagramas Arquitectónicos**
- Servidor Flask adicional para visualizar diagramas Mermaid
- Flujo conversacional documentado
- Detalles técnicos interactivos

✅ **Documentación Completa**
- Explicación del PLN y su utilidad
- Detalles técnicos (modelos, parámetros)
- Instrucciones de instalación y uso

---

## 🚀 Inicio Rápido

### Requisitos previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Clave de API de Google Gemini (obtén una [aquí](https://ai.google.dev/))

### Instalación (5 minutos)

1. **Clonar o descargar el repositorio:**
```bash
git clone https://github.com/usuario/asistente-rag-tea.git
cd asistente-rag-tea
```

2. **Crear archivo `.env` con tu clave de API:**
```bash
cp .env.example .env
# Edita .env y añade tu GOOGLE_API_KEY
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Arrancar el servidor:**
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 9000
```

5. **Abrir en el navegador:**
```
http://127.0.0.1:9000
```

---

## 📚 Uso

### Consulta RAG (Preguntas sobre trámites)
**UI Web:**
- Ve a http://127.0.0.1:9000
- Escribe tu pregunta en el textarea
- Haz clic en "Consultar"
- Visualiza la respuesta y las fuentes

**Desde API (Terminal):**
```bash
curl -X POST "http://127.0.0.1:9000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "pregunta": "¿Cuáles son los pasos para solicitar reconocimiento de discapacidad?",
    "usuario_id": "usuario_juan"
  }'
```

### Usar el Agente (Crear solicitudes)
**Desde API:**
```bash
curl -X POST "http://127.0.0.1:9000/api/agent" \
  -H "Content-Type: application/json" \
  -d '{
    "instruccion": "Generar solicitud de reconocimiento de discapacidad",
    "usuario_id": "usuario_juan"
  }'
```

**Resultado:** Se crea un archivo en `data/solicitudes/solicitud_usuario_juan_<timestamp>.json`

### Ver diagramas arquitectónicos
```bash
python .\scripts\serve_diagram.py
# Abre: http://127.0.0.1:5001
```

---

## 🏗️ Estructura del Proyecto

```
rag_teandalucia/
├── main.py                          # API FastAPI principal
├── requirements.txt                 # Dependencias
├── DOCUMENTACION.md                 # Documentación técnica detallada
├── README.md                        # Este archivo
├── .env.example                     # Plantilla de variables de entorno
├── .gitignore                       # Archivos a excluir del repo
│
├── config/
│   └── settings.py                  # Configuración centralizada
│
├── services/
│   ├── rag_service.py               # Servicio RAG (embeddings + LLM)
│   ├── agent_service.py             # Agente simple para crear solicitudes
│   ├── embeddings.py                # Generación de embeddings
│   ├── chunking.py                  # Fragmentación de textos
│   ├── process_pdfs.py              # Extracción y limpieza de PDFs
│   └── perfil_service.py            # Gestión de perfiles de usuario
│
├── scripts/
│   ├── serve_diagram.py             # Servidor Flask para diagramas Mermaid
│   ├── test_agent.py                # Tests del agente simple
│   └── INSTRUCCIONES_FLASK.md       # Guía de uso de Flask
│
├── static/
│   ├── index.html                   # UI principal
│   ├── css/
│   │   └── style.css                # Estilos
│   └── js/
│       └── script.js                # Lógica del frontend
│
└── data/
    ├── perfiles/                    # Historiales de usuarios (JSON)
    ├── solicitudes/                 # Solicitudes generadas (JSON)
    ├── data_clean/                  # Texto limpio de PDFs
    └── embeddings/                  # Índice vectorial
```

---

## 🔧 Detalles Técnicos

### Stack Tecnológico
| Componente | Tecnología | Versión |
|------------|-----------|---------|
| **LLM** | Google Gemini | 2.5-flash-lite |
| **Embeddings** | Sentence-Transformers | paraphrase-multilingual-MiniLM-L12-v2 |
| **Vectorstore** | NumPy (local) | Escalable a Chroma/FAISS |
| **Framework Web** | FastAPI | 0.100+ |
| **Servidor** | Uvicorn | standard |
| **Visualización** | Flask + Mermaid | 1.0+ |
| **Frontend** | HTML/CSS/JavaScript | Vanilla JS |

### Parámetros RAG
- **Chunk Size:** 1000 caracteres
- **Chunk Overlap:** 200 caracteres
- **Top-K Chunks:** 4 fragmentos más relevantes
- **Similitud:** Cosine Similarity (scikit-learn)

### Endpoints Disponibles
| Método | Endpoint | Descripción |
|--------|----------|-----------|
| GET | `/` | Sirve la UI principal |
| GET | `/api/health` | Estado del servidor |
| POST | `/api/reindex` | Reconstruye índice desde PDFs |
| POST | `/api/query` | Consulta RAG |
| POST | `/api/agent` | Ejecuta agente autónomo |
| GET | `/api/historial` | Historial de usuario |

---

## 🧠 Procesamiento del Lenguaje Natural (PLN)

### ¿Por qué PLN?
El PLN permite a máquinas:
1. **Comprender significado** — más allá de palabras clave exactas
2. **Buscar semánticamente** — encontrar información relevante incluso con formulaciones diferentes
3. **Generar lenguaje natural** — producir respuestas coherentes y accesibles
4. **Automatizar tareas** — procesar documentos sin intervención manual

### En este proyecto
- **Extracción:** Limpieza de PDFs
- **Vectorización:** Embeddings semánticos
- **Búsqueda:** Similitud de coseno en espacios vectoriales
- **Generación:** LLM para respuestas coherentes
- **Accesibilidad:** Lenguaje sencillo para familias

---

## 📖 Documentación Completa

Para información más detallada, consulta:
- **[DOCUMENTACION.md](DOCUMENTACION.md)** — Especificaciones técnicas, diagrama Mermaid, PLN, pipeline
- **[scripts/INSTRUCCIONES_FLASK.md](scripts/INSTRUCCIONES_FLASK.md)** — Cómo ejecutar el servidor de diagramas

---

## 🔐 Seguridad

### Variables de Entorno
- **Nunca** subas `.env` con claves reales al repositorio
- Usa `.env.example` como plantilla
- `.gitignore` excluye automáticamente `.env`

### Obtener claves de API
1. **Google Gemini:** [https://ai.google.dev/](https://ai.google.dev/)
   - Crea un proyecto en Google Cloud
   - Activa la API de Generative AI
   - Genera una clave de API

2. **Monitorización (opcional):**
   - LangSmith: [https://smith.langchain.com](https://smith.langchain.com)
   - Langfuse: [https://langfuse.com](https://langfuse.com)

---

## 🧪 Testing

Prueba rápida del agente sin servidor:
```bash
python scripts/test_agent.py
```

Verifica que se crea un archivo en `data/solicitudes/`.

---

## 📊 Mejoras Futuras

- [ ] Migración completa a LangChain (`RetrievalQA` + `Chroma`)
- [ ] Agente avanzado con múltiples herramientas
- [ ] Monitorización con LangSmith o Langfuse
- [ ] Tests unitarios e integración
- [ ] GitHub Actions para CI/CD
- [ ] Despliegue en Docker
- [ ] UI mejorada con React/Vue
- [ ] Autenticación de usuarios

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commits con mensajes claros
4. Push y crea un Pull Request

---

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto y Soporte

- **GitHub Issues:** Para reportar bugs o sugerir mejoras
- **Documentación:** [DOCUMENTACION.md](DOCUMENTACION.md)
- **Email:** [tu-email@example.com] (opcional)

---

## 🙏 Agradecimientos

- Google Gemini por el modelo LLM
- Sentence-Transformers por embeddings
- FastAPI por el framework web
- comunidad de código abierto

---

**Desarrollado con ❤️ para familias con miembros con autismo en Andalucía**

