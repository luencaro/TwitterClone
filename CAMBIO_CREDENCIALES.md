# 🔒 Cambio de Credenciales - Guía de Seguridad

## ✅ Cambios Realizados

### 1. **Archivos .env Removidos de GitHub**
- `.env` y `.env.backup` eliminados del tracking de git
- Ahora solo existe `.env.example` (sin credenciales reales)

### 2. **.gitignore Actualizado**
Ahora ignora:
- `.env`
- `.env.backup`
- `.env.local`
- `.env.*.local`

### 3. **Nuevas Credenciales Generadas**

#### SECRET_KEY de Django (actualizada en `.env`)
```
%57xh38rDrGmLqMAVTWNt86!!B*lvFoDM8%ZrcC(bZ=I_y!Cut
```

#### Contraseña de Neo4j (actualizada en `.env`)
```
NuevaNeo4jPass2024!Segura
```

---

## 🔧 Cómo Aplicar los Cambios en Neo4j

### Opción 1: Recrear el Contenedor (RECOMENDADO)

Si tienes datos de prueba que puedes perder:

```bash
# 1. Detener y eliminar el contenedor actual
sudo systemctl start docker
sudo docker stop neo4j-twitterclone
sudo docker rm neo4j-twitterclone

# 2. Opcional: Limpiar datos antiguos
sudo rm -rf ~/neo4j/data ~/neo4j/logs

# 3. Crear nuevo contenedor con nueva contraseña
./start_neo4j.sh

# 4. Esperar que Neo4j inicie (30-60 segundos)
echo "Esperando a que Neo4j inicie..."
sleep 40

# 5. Re-migrar datos desde Django
source venv/bin/activate
python manage.py migrate_to_neo4j --clear
python manage.py create_dummy_data
```

### Opción 2: Cambiar Contraseña en Contenedor Existente

Si tienes datos importantes en Neo4j:

```bash
# 1. Iniciar Docker
sudo systemctl start docker

# 2. Acceder al contenedor
sudo docker exec -it neo4j-twitterclone cypher-shell -u neo4j -p password123

# 3. Dentro de cypher-shell, ejecutar:
ALTER CURRENT USER SET PASSWORD FROM 'password123' TO 'NuevaNeo4jPass2024!Segura';
:exit

# 4. Reiniciar contenedor
sudo docker restart neo4j-twitterclone
```

---

## ✅ Verificar que Todo Funciona

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Probar conexión a Django
python manage.py check

# 3. Probar conexión a Neo4j
python manage.py shell << 'EOF'
from blog.neo4j_connection import test_neo4j_connection
test_neo4j_connection()
EOF

# 4. Iniciar servidor
python manage.py runserver
```

---

## 🚨 IMPORTANTE: Qué NO Hacer

❌ **NO** compartas el archivo `.env` con nadie  
❌ **NO** subas `.env` a GitHub (ya está en .gitignore)  
❌ **NO** uses las credenciales antiguas:
   - `password123` (Neo4j) - COMPROMETIDA
   - `*n*f0zqlu+cgn&m*sd3^qkz9b=nw6db(tfo$156o9ag-%2f_eq` (Django) - COMPROMETIDA

---

## 📝 Para Otros Desarrolladores

Si alguien clona el repositorio:

```bash
# 1. Clonar repo
git clone https://github.com/luencaro/TwitterClone.git
cd TwitterClone

# 2. Copiar .env.example a .env
cp .env.example .env

# 3. PEDIRTE las credenciales reales
# Tú les compartes las credenciales por canal seguro (Slack, email, etc.)

# 4. Editar .env con las credenciales reales
nano .env
```

---

## ✅ Estado Actual

- [x] `.gitignore` actualizado
- [x] `.env` y `.env.backup` removidos de git
- [x] `.env.example` creado (sin credenciales)
- [x] Nueva SECRET_KEY generada
- [x] Nueva contraseña de Neo4j generada
- [x] `start_neo4j.sh` actualizado
- [ ] **PENDIENTE:** Recrear contenedor Neo4j con nueva contraseña
- [ ] **PENDIENTE:** Hacer commit y push de cambios seguros

---

## 🔐 Próximos Pasos

1. **Aplicar cambios en Neo4j** (ver opciones arriba)
2. **Hacer commit de cambios seguros:**
   ```bash
   git status
   git add .gitignore .env.example start_neo4j.sh
   git commit -m "🔒 Security: Remove .env files and update credentials"
   git push origin main
   ```

3. **Verificar en GitHub** que `.env` ya no aparece en el repo

---

**Fecha de cambio:** 31 de Octubre, 2025  
**Archivos afectados:** `.env`, `.env.example`, `.gitignore`, `start_neo4j.sh`
