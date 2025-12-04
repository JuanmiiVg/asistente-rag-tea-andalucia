# 📤 Instrucciones para subir a GitHub

## ✅ SEGURIDAD: Verificación pre-push

**ANTES de cualquier cosa, ejecuta:**
```powershell
python scripts/verificar_seguridad.py
```

**Deberías ver:**
```
✅ TODO OK: Es seguro hacer git push
```

Si ves `❌ PROBLEMAS DETECTADOS`, revisa qué falta antes de continuar.

---

## 📝 Pasos para subir (por primera vez)

### Paso 1: Inicializar Git (si no está hecho)
```powershell
cd C:\Users\juanm\Documents\BigData\rag_Proyecto\rag_teandalucia
git init
git config user.name "Tu Nombre"
git config user.email "tu.email@example.com"
```

### Paso 2: Verificar estado antes de staged
```powershell
git status
```

**Deberías ver:**
```
On branch master

Untracked files:
  (use "git add <file>..." to include in what will be commited)
        README.md
        DOCUMENTACION.md
        main.py
        ... (otros archivos)

nothing added to commit but untracked files present (tracking what will be committed)
```

**IMPORTANTE: `.env` NO debe aparecer en esta lista (debe estar ignorado por `.gitignore`)**

### Paso 3: Añadir todos los archivos (excepto los ignorados)
```powershell
git add .
```

**Verificar que `.env` no está staged:**
```powershell
git diff --cached --name-only | findstr .env
```

Si aparece `.env`, ejecuta:
```powershell
git reset .env
```

### Paso 4: Commit inicial
```powershell
git commit -m "Inicial: Asistente RAG con agente autónomo, logging, documentación y seguridad"
```

### Paso 5: Cambiar rama a main (GitHub por defecto)
```powershell
git branch -M main
```

### Paso 6: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Llena la información:
   - **Repository name:** `asistente-rag-tea-andalucia` (o tu nombre preferido)
   - **Description:** "Chatbot RAG con agente autónomo para asistir a familias con autismo en Andalucía"
   - **Public** (para ejercicio académico)
   - No inicialices con README (ya tienes uno)

3. Click en "Create repository"

### Paso 7: Conectar y subir a GitHub

Copia y ejecuta los comandos que GitHub te muestra (serán algo como):

```powershell
git remote add origin https://github.com/tu-usuario/asistente-rag-tea-andalucia.git
git branch -M main
git push -u origin main
```

**Output esperado:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 8 threads
...
To https://github.com/tu-usuario/asistente-rag-tea-andalucia.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## ✨ Verificar que todo subió correctamente

### En línea de comandos:
```powershell
git remote -v
# Deberías ver:
# origin  https://github.com/tu-usuario/asistente-rag-tea-andalucia.git (fetch)
# origin  https://github.com/tu-usuario/asistente-rag-tea-andalucia.git (push)

git log --oneline -5
# Deberías ver tu commit
```

### En GitHub.com:
1. Abre tu repo: `https://github.com/tu-usuario/asistente-rag-tea-andalucia`
2. Verifica que ves:
   - ✅ `README.md` mostrado como descripción
   - ✅ `DOCUMENTACION.md` visible
   - ✅ `requirements.txt`
   - ✅ `.gitignore` aplicado (no ves `.env`)
   - ✅ `main.py`, servicios, scripts
   - ✅ Folders: `static/`, `services/`, `scripts/`, `config/`

---

## 📋 Checklist pre-push FINAL

Antes de hacer `git push`:

- [ ] Ejecuté `python scripts/verificar_seguridad.py` y dice OK
- [ ] `.env` **NO está** en `git status`
- [ ] `.env` **SÍ está** en `.gitignore`
- [ ] No hay `*.pyc` o `__pycache__` staged
- [ ] El commit tiene un mensaje descriptivo
- [ ] Creé el repositorio en GitHub
- [ ] Copié el remote URL correcto

---

## 🔄 Para futuros cambios (después del primer push)

Después de este primer push, para hacer cambios:

```powershell
# 1. Modificar archivos (ej. agregar features)
# 2. Verificar cambios
git status

# 3. Agregar cambios
git add .

# 4. Commit
git commit -m "Descripción clara del cambio"

# 5. Push
git push origin main
```

---

## ⚠️ Si algo sale mal

### "fatal: The current branch master has no upstream branch"
```powershell
git push -u origin main
```

### ".env fue commiteado accidentalmente"
```powershell
# Opción 1: Quitarlo del último commit (si no hiciste push aún)
git reset --soft HEAD~1
git reset .env
git commit -m "Commit sin .env"

# Opción 2: Limpieza del historio (si ya hiciste push)
git filter-repo --path .env --invert-paths
git push --force origin main
# ⚠️ ADVERTENCIA: Force push reescribe el historio
```

### No recuerdas la contraseña
```powershell
# Usar token personal en lugar de contraseña
# 1. Ve a GitHub > Settings > Developer settings > Personal access tokens
# 2. Genera un token (con permisos: repo)
# 3. Usa como contraseña cuando git lo pida
```

---

## 🎯 URLs y referencias

- **Tu repositorio:** `https://github.com/tu-usuario/asistente-rag-tea-andalucia`
- **GitHub Docs (en español):** https://docs.github.com/es
- **Generar token personal:** https://github.com/settings/tokens

---

**¡Listo! Ya tendrás tu proyecto en GitHub 🚀**
