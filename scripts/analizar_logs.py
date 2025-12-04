"""
Script para analizar y visualizar estadísticas de las interacciones del chatbot.
Lee logs/interactions.jsonl y muestra métricas, tendencias y reportes.

Ejecutar: python scripts/analizar_logs.py
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import statistics

# Ruta del log
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
INTERACTIONS_LOG = LOGS_DIR / "interactions.jsonl"


def cargar_interacciones():
    """Carga todos los registros del archivo de interacciones."""
    registros = []
    if not INTERACTIONS_LOG.exists():
        print(f"❌ Archivo no encontrado: {INTERACTIONS_LOG}")
        return registros
    
    try:
        with open(INTERACTIONS_LOG, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    registros.append(json.loads(line.strip()))
    except Exception as e:
        print(f"❌ Error al leer logs: {e}")
    
    return registros


def analizar_logs(registros):
    """Analiza los registros y calcula estadísticas."""
    if not registros:
        print("⚠️  No hay registros para analizar.")
        return
    
    print("\n" + "="*70)
    print("📊 ANÁLISIS DE INTERACCIONES DEL CHATBOT")
    print("="*70)
    
    # Estadísticas generales
    print(f"\n📈 Estadísticas Generales")
    print(f"   Total de interacciones: {len(registros)}")
    print(f"   Primer registro: {registros[0].get('timestamp', 'N/A')}")
    print(f"   Último registro: {registros[-1].get('timestamp', 'N/A')}")
    
    # Usuarios únicos
    usuarios = set(r.get('usuario_id', 'desconocido') for r in registros)
    print(f"   Usuarios únicos: {len(usuarios)}")
    
    # Endpoints
    endpoints = Counter(r.get('endpoint', 'desconocido') for r in registros)
    print(f"\n🔌 Llamadas por endpoint:")
    for endpoint, count in endpoints.most_common():
        print(f"   {endpoint}: {count}")
    
    # Latencias
    latencias = [r.get('latencia_ms', 0) for r in registros if r.get('latencia_ms')]
    if latencias:
        print(f"\n⏱️  Latencias (ms):")
        print(f"   Mínima: {min(latencias):.2f}ms")
        print(f"   Máxima: {max(latencias):.2f}ms")
        print(f"   Promedio: {statistics.mean(latencias):.2f}ms")
        print(f"   Mediana: {statistics.median(latencias):.2f}ms")
    
    # Acciones del agente
    acciones_agente = Counter(r.get('accion_agente', 'N/A') for r in registros if r.get('endpoint') == '/api/agent')
    if acciones_agente:
        print(f"\n🤖 Acciones del agente:")
        for accion, count in acciones_agente.most_common():
            print(f"   {accion}: {count}")
    
    # Fuentes más consultadas
    todas_las_fuentes = []
    for r in registros:
        todas_las_fuentes.extend(r.get('fuentes', []))
    
    fuentes_count = Counter(todas_las_fuentes)
    if fuentes_count:
        print(f"\n📚 Documentos más consultados:")
        for fuente, count in fuentes_count.most_common(5):
            print(f"   {fuente}: {count} veces")
    
    # Usuarios más activos
    usuarios_count = Counter(r.get('usuario_id', 'desconocido') for r in registros)
    if usuarios_count:
        print(f"\n👥 Usuarios más activos:")
        for usuario, count in usuarios_count.most_common(5):
            print(f"   {usuario}: {count} interacciones")
    
    # Errores (si hay)
    errores = [r for r in registros if 'error' in r.get('metadata', {}).get('status', '').lower()]
    if errores:
        print(f"\n❌ Registros con errores: {len(errores)}")
    
    print("\n" + "="*70)


def generar_reporte_csv(registros):
    """Genera un CSV para análisis en Excel."""
    if not registros:
        return
    
    csv_path = LOGS_DIR / "interacciones_reporte.csv"
    
    try:
        import csv
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'endpoint', 'usuario_id', 'latencia_ms', 'accion_agente'
            ])
            writer.writeheader()
            for r in registros:
                writer.writerow({
                    'timestamp': r.get('timestamp', ''),
                    'endpoint': r.get('endpoint', ''),
                    'usuario_id': r.get('usuario_id', ''),
                    'latencia_ms': r.get('latencia_ms', ''),
                    'accion_agente': r.get('accion_agente', '')
                })
        print(f"\n✅ Reporte CSV generado: {csv_path}")
    except Exception as e:
        print(f"\n⚠️  Error generando CSV: {e}")


def mostrar_ultimas_interacciones(registros, n=5):
    """Muestra las últimas N interacciones."""
    if not registros:
        return
    
    print(f"\n📝 Últimas {n} interacciones:")
    print("-" * 70)
    
    for i, r in enumerate(registros[-n:], 1):
        timestamp = r.get('timestamp', 'N/A')
        usuario = r.get('usuario_id', 'desconocido')
        endpoint = r.get('endpoint', 'N/A')
        latencia = r.get('latencia_ms', 'N/A')
        entrada = r.get('entrada', '')[:50]
        
        print(f"\n{i}. [{timestamp}] {usuario} ({endpoint})")
        print(f"   Entrada: {entrada}...")
        print(f"   Latencia: {latencia}ms")


if __name__ == '__main__':
    print("\n🚀 Analizando logs de interacciones...")
    
    registros = cargar_interacciones()
    
    if registros:
        analizar_logs(registros)
        mostrar_ultimas_interacciones(registros, n=3)
        generar_reporte_csv(registros)
    else:
        print("\n⚠️  No hay interacciones registradas aún.")
        print("   Usa el chatbot (http://127.0.0.1:9000) y vuelve a intentar.")
    
    print(f"\n📂 Archivo de logs: {INTERACTIONS_LOG}")
    print()
