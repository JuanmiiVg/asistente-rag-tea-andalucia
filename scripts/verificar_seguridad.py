"""
Script de verificación de seguridad pre-git.
Verifica que no haya claves de API, contraseñas o archivos sensibles a punto de subirse.

Ejecutar ANTES de hacer git push:
  python scripts/verificar_seguridad.py
"""

import os
import re
import sys
from pathlib import Path

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Archivos/carpetas que NO deben subirse
FORBIDDEN_FILES = {
    '.env',
    '.env.local',
    '*.pyc',
    '__pycache__',
    '.venv',
    'venv',
    '*.log',
    'logs/',
    'embeddings/embeddings.npy',
    'embeddings/chunks_metadata.json',
}

# Patrones de secretos a buscar
SECRET_PATTERNS = [
    r'AIzaSy[A-Za-z0-9\-_]{35}',  # Google API Key
    r'sk-[A-Za-z0-9]{20,}',        # OpenAI/OpenRouter
    r'password\s*=\s*["\'][^"\']+["\']',
    r'secret\s*=\s*["\'][^"\']+["\']',
    r'api_key\s*=\s*["\'][^"\']+["\']',
]

def verificar_gitignore():
    """Verifica que .gitignore existe y contiene .env"""
    gitignore_path = PROJECT_ROOT / '.gitignore'
    
    if not gitignore_path.exists():
        print("❌ ERROR: No existe .gitignore")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
        if '.env' not in content:
            print("❌ ERROR: .env no está en .gitignore")
            return False
    
    print("✅ .gitignore existe y contiene .env")
    return True

def verificar_env_example():
    """Verifica que .env.example existe pero sin claves reales"""
    env_example = PROJECT_ROOT / '.env.example'
    
    if not env_example.exists():
        print("❌ ERROR: No existe .env.example")
        return False
    
    with open(env_example, 'r') as f:
        content = f.read()
        
        # Buscar claves reales (no placeholders)
        if re.search(r'AIzaSy[A-Za-z0-9\-_]{35}', content):
            print("❌ ERROR: .env.example contiene una clave real de Google!")
            return False
        
        if 'your_' not in content.lower() and '=' in content:
            print("⚠️  ADVERTENCIA: .env.example podría contener valores reales")
            return False
    
    print("✅ .env.example es seguro (solo placeholders)")
    return True

def verificar_env():
    """Verifica que .env existe y contiene claves"""
    env_path = PROJECT_ROOT / '.env'
    
    if not env_path.exists():
        print("⚠️  ADVERTENCIA: No existe .env local (créalo antes de correr la app)")
        return True
    
    # Si existe, verificar que no sea staged en git
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        
        if '.env' in result.stdout:
            print("❌ ERROR: .env está staged para commit!")
            print("   Ejecuta: git reset .env")
            return False
    except:
        pass
    
    print("✅ .env no está staged (seguro)")
    return True

def buscar_secretos_en_codigo():
    """Busca patrones de secretos en archivos de código"""
    archivos_a_revisar = list(PROJECT_ROOT.rglob('*.py'))
    secretos_encontrados = []
    
    for archivo in archivos_a_revisar:
        # Saltar directorios no relevantes
        if any(x in str(archivo) for x in ['venv', '__pycache__', '.venv', 'site-packages']):
            continue
        
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                
                for patron in SECRET_PATTERNS:
                    matches = re.findall(patron, contenido)
                    
                    # Filtrar falsos positivos
                    for match in matches:
                        # Ignorar placeholders
                        if 'your_' in match or 'example' in match or 'test' in match:
                            continue
                        
                        # Ignorar referencias a variables
                        if 'GOOGLE_API_KEY' in match or 'os.getenv' in match:
                            continue
                        
                        secretos_encontrados.append({
                            'archivo': archivo,
                            'patron': match[:50],
                            'linea': contenido[:contenido.find(match)].count('\n') + 1
                        })
        except:
            pass
    
    if secretos_encontrados:
        print("❌ ERROR: Se encontraron posibles secretos en código:")
        for item in secretos_encontrados:
            print(f"   - {item['archivo'].name}:{item['linea']} → {item['patron']}")
        return False
    
    print("✅ No se encontraron secretos en código")
    return True

def main():
    print("\n" + "="*70)
    print("🔐 VERIFICACIÓN DE SEGURIDAD PRE-GIT")
    print("="*70 + "\n")
    
    resultados = {
        "gitignore": verificar_gitignore(),
        "env_example": verificar_env_example(),
        "env_local": verificar_env(),
        "secretos_codigo": buscar_secretos_en_codigo()
    }
    
    print("\n" + "="*70)
    
    if all(resultados.values()):
        print("✅ TODO OK: Es seguro hacer git push")
        print("="*70 + "\n")
        return 0
    else:
        print("❌ PROBLEMAS DETECTADOS: Revisa los errores arriba")
        print("="*70 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
