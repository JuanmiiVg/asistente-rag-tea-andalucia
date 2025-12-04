# 📊 Monitorización del Chatbot — Sistema de Logging JSON

## Descripción
El chatbot registra automáticamente cada interacción (consultas RAG y acciones del agente) en archivos JSON.

**Ubicación:** `logs/` 
- `logs/interactions.jsonl` — Cada línea es un JSON con una interacción
- `logs/errors.log` — Errores en formato log estándar

## ¿Qué se registra?

### Por cada consulta RAG (`/api/query`):
```json
{
  "timestamp": "2025-12-04T18:30:45.123Z",
  "endpoint": "/api/query",
  "usuario_id": "usuario_juan",
  "entrada": "¿Cuáles son los pasos para solicitar reconocimiento?",
  "salida": "Los pasos son: 1) Contactar con... 2) Presentar documentos...",
  "latencia_ms": 2340.56,
  "fuentes": ["Res_TEA.txt"],
  "accion_agente": null,
  "metadata": {"model": "gemini-2.5-flash-lite"}
}
```

### Por cada acción del agente (`/api/agent`):
```json
{
  "timestamp": "2025-12-04T18:31:20.789Z",
  "endpoint": "/api/agent",
  "usuario_id": "usuario_juan",
  "entrada": "Generar solicitud de reconocimiento",
  "salida": "data/solicitudes/solicitud_usuario_juan_20251204T183120Z.json",
  "latencia_ms": 1567.89,
  "fuentes": ["Res_TEA.txt"],
  "accion_agente": "created_solicitud",
  "metadata": {"action_type": "created_solicitud"}
}
```

### Errores:
```
2025-12-04 18:32:15,234 - services.logger_service - ERROR - [/api/query] User: usuario_juan | Type: QueryError | Message: Índice no disponible
```

---

## 📈 Cómo analizar los logs

### Opción 1: Script automático (recomendado)
```powershell
cd C:\Users\juanm\Documents\BigData\rag_Proyecto\rag_teandalucia
python scripts/analizar_logs.py
```

**Genera:**
- 📊 Estadísticas de interacciones
- ⏱️ Latencias (mín/máx/promedio)
- 🤖 Acciones del agente
- 📚 Documentos más consultados
- 👥 Usuarios más activos
- 📄 CSV exportable (`interacciones_reporte.csv`)

### Opción 2: Abrir en Excel
1. Abre `logs/interactions.jsonl` con cualquier editor de texto
2. Copia el contenido a Excel
3. Usa "Datos > Análisis rápido" para visualizaciones

### Opción 3: Script personalizado (Python)
```python
from services.logger_service import read_interactions_log

registros = read_interactions_log()
for r in registros:
    print(f"{r['timestamp']} - {r['usuario_id']} - {r['latencia_ms']}ms")
```

---

## 📝 Estructura del archivo `interactions.jsonl`

- **Formato:** JSONL (JSON Lines) — cada línea es un JSON válido
- **Codificación:** UTF-8
- **Acción:** Append — los nuevos registros se añaden al final
- **No requiere:** Dependencias externas (solo JSON de Python estándar)

---

## 🔍 Ejemplos de análisis

### Encontrar interacciones lentas
```python
from services.logger_service import read_interactions_log

registros = read_interactions_log()
lentas = [r for r in registros if r.get('latencia_ms', 0) > 3000]
print(f"Consultas que tardaron > 3s: {len(lentas)}")
```

### Ver acciones del agente
```python
registros = read_interactions_log()
acciones = [r for r in registros if r.get('endpoint') == '/api/agent']
print(f"Total acciones agente: {len(acciones)}")
for r in acciones:
    print(f"  - {r['timestamp']}: {r['accion_agente']}")
```

### Historial por usuario
```python
registros = read_interactions_log()
usuario_juan = [r for r in registros if r.get('usuario_id') == 'usuario_juan']
print(f"Interacciones de usuario_juan: {len(usuario_juan)}")
```

---

## 📊 Script `analizar_logs.py`

Ejecutar:
```bash
python scripts/analizar_logs.py
```

**Salida:**
```
======================================================================
📊 ANÁLISIS DE INTERACCIONES DEL CHATBOT
======================================================================

📈 Estadísticas Generales
   Total de interacciones: 15
   Primer registro: 2025-12-04T18:30:45.123Z
   Último registro: 2025-12-04T18:35:20.456Z
   Usuarios únicos: 3

🔌 Llamadas por endpoint:
   /api/query: 10
   /api/agent: 5

⏱️  Latencias (ms):
   Mínima: 234.50ms
   Máxima: 4567.80ms
   Promedio: 1892.34ms
   Mediana: 1200.50ms

🤖 Acciones del agente:
   created_solicitud: 3
   answer_only: 2

📚 Documentos más consultados:
   Res_TEA.txt: 15 veces

👥 Usuarios más activos:
   usuario_juan: 8 interacciones
   usuario_maria: 4 interacciones
   test_user: 3 interacciones

📝 Últimas 3 interacciones:
1. [2025-12-04T18:35:20.456Z] usuario_juan (/api/query)
   Entrada: ¿Cuáles son los pasos para...
   Latencia: 2345ms

...

✅ Reporte CSV generado: logs/interacciones_reporte.csv
```

---

## 🔄 Limpieza de logs (opcional)

Para limpiar los logs históricos:
```powershell
Remove-Item logs/interactions.jsonl -Force
Remove-Item logs/errors.log -Force
```

El sistema recreará los archivos automáticamente en la próxima interacción.

---

## 📌 Notas importantes

1. **Privacidad:** Los logs contienen preguntas/respuestas de usuarios. Guardalos de forma segura.
2. **Tamaño:** El archivo `interactions.jsonl` crece con cada interacción (~0.5-1KB por registro).
3. **Rotación:** Para logs grandes, considera rotar archivos periódicamente (ej. log_2025_12.jsonl).
4. **Análisis:** El CSV exportado es ideal para análisis en Excel/Power BI.

---

## 🎯 Cómo integrar esto en tu documentación

En `DOCUMENTACION.md`, añade:
```markdown
## Monitorización y Análisis

El chatbot registra automáticamente cada interacción en `logs/interactions.jsonl`.

Para ver estadísticas:
\`\`\`bash
python scripts/analizar_logs.py
\`\`\`

Ver: [LOGGING.md](LOGGING.md)
```

---

**Para más detalles:** Consulta `services/logger_service.py` y `scripts/analizar_logs.py`
