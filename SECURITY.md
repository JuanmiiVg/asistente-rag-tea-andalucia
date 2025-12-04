# ⚠️ NOTA DE SEGURIDAD — Eliminar clave del repositorio

## Problema detectado
El archivo `.env` **contiene una clave real de Google API** que puede haber sido expuesta si fue subida a GitHub.

## Pasos para resolver (URGENTE)

### 1. Rotar la clave de Google Gemini
1. Ve a [Google AI Studio](https://ai.google.dev/)
2. Ve a "Manage API keys"
3. Elimina la clave comprometida
4. Genera una nueva clave

### 2. Limpiar el historial de Git (si ya fue subida)
Si el `.env` fue commiteado al repositorio, limpiar el historio:

```bash
# Opción A: git filter-repo (recomendado, más rápido)
pip install git-filter-repo
git filter-repo --path .env --invert-paths

# Opción B: git filter-branch (alternativa, más lenta)
git filter-branch --tree-filter 'rm -f .env' HEAD
git reflog expire --expire=now --all
git gc --aggressive --prune=now
```

### 3. Force push al repositorio
```bash
git push origin --force --all
```

⚠️ **Advertencia:** Force push reescribe el historio. Solo hazlo si eres dueño del repo o tienes permisos.

### 4. Verificar configuración
```bash
# Asegúrate de que .env está en .gitignore
cat .gitignore | grep "\.env"

# Verifica que .env.example NO contiene secretos reales
cat .env.example
```

### 5. Crear nuevo .env seguro
```bash
cp .env.example .env
# Edita .env y añade la NUEVA clave de Google Gemini
```

---

## Cómo evitar esto en el futuro

1. **Siempre usa `.env` en `.gitignore`**
   ```
   # .gitignore
   .env
   .env.local
   ```

2. **Usa `.env.example` como plantilla**
   ```bash
   cp .env.example .env
   ```

3. **Pre-commit hook (opcional pero recomendado)**
   ```bash
   npm install husky lint-staged --save-dev
   npx husky install
   npx husky add .husky/pre-commit 'git diff --cached --name-only | grep -q "\.env$" && echo "ERROR: .env no puede ser commiteado" && exit 1'
   ```

4. **GitHub Secrets para CI/CD**
   Si usas GitHub Actions, no hardcodees las claves. Usa secretos:
   ```yaml
   env:
     GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
   ```

---

## Checklist de seguridad

- [ ] Nueva clave de Google Gemini generada
- [ ] Clave antigua deletreada de Google Cloud
- [ ] `.env` limpiado del historio de Git
- [ ] `.env` está en `.gitignore`
- [ ] `.env.example` NO contiene secretos reales
- [ ] `.gitignore` revisado (no hay `__pycache__`, `*.pyc`, etc.)
- [ ] Mensaje de commit menciona la limpieza de seguridad

---

**Para más información:** [OWASP - Secrets Management](https://owasp.org/www-community/Sensitive_Data_Exposure)
