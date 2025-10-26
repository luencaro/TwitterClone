# ⚡ Inicio Rápido - TwitterClone con Neo4j

## 🎯 Objetivo
Tener la aplicación corriendo en **menos de 10 minutos**.

## 📋 Pre-requisitos
- Python 3.8+ instalado
- Docker instalado (para Neo4j)
- Terminal/Consola

## 🚀 Pasos de Instalación

### 1️⃣ Iniciar Neo4j con Docker (2 minutos)

```bash
docker run \
    --name neo4j-twitterclone \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/password123 \
    neo4j:5.14
```

**Verificar que funciona:**
- Abre http://localhost:7474
- Usuario: `neo4j`
- Contraseña: `password123`

### 2️⃣ Clonar y Configurar Proyecto (3 minutos)

```bash
# Navegar al directorio del proyecto (ya lo tienes)
cd "/home/luencaro/Programing/My Repositories/College/Base de Datos/TwitterClone"

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Configurar Variables de Entorno (1 minuto)

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar (si usas diferentes credenciales)
nano .env
```

Contenido mínimo de `.env`:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
SECRET_KEY=django-insecure-dev-key-change-in-production
```

### 4️⃣ Configurar Base de Datos (2 minutos)

```bash
# Aplicar migraciones de Django
python manage.py migrate

# Crear superusuario (sigue las instrucciones)
python manage.py createsuperuser
```

### 5️⃣ (Opcional) Datos de Prueba (1 minuto)

```bash
# Crear datos de ejemplo
python manage.py create_dummy_data

# Migrar a Neo4j
python manage.py migrate_to_neo4j --clear
```

### 6️⃣ Iniciar Servidor (30 segundos)

```bash
python manage.py runserver
```

## 🎉 ¡Listo!

Abre tu navegador en: **http://localhost:8000**

## 📍 URLs Importantes

| URL | Descripción |
|-----|-------------|
| http://localhost:8000 | Aplicación principal |
| http://localhost:8000/admin | Panel de administración Django |
| http://localhost:7474 | Navegador de Neo4j |
| http://localhost:8000/analytics/ | Análisis de red |
| http://localhost:8000/interests/ | Gestión de intereses |

## 🔑 Credenciales por Defecto

**Django Admin:**
- Usuario: El que creaste con `createsuperuser`
- Contraseña: La que estableciste

**Neo4j Browser:**
- URL: http://localhost:7474
- Usuario: `neo4j`
- Contraseña: `password123` (la que configuraste)

## ✅ Verificación Rápida

### Test 1: Conexión Django
```bash
python manage.py check
```
Debería mostrar: **System check identified no issues**

### Test 2: Conexión Neo4j
```bash
python -c "from blog.neo4j_connection import init_neo4j_connection; print('✓ OK' if init_neo4j_connection() else '✗ Error')"
```
Debería mostrar: **✓ Conexión exitosa con Neo4j**

### Test 3: Verificar Datos en Neo4j
Abre Neo4j Browser (http://localhost:7474) y ejecuta:
```cypher
MATCH (n) RETURN count(n) as total_nodos
```

## 🐛 Solución Rápida de Problemas

### ❌ Error: "No module named 'neomodel'"
```bash
pip install -r requirements.txt --force-reinstall
```

### ❌ Error: "Connection refused" (Neo4j)
```bash
# Verificar que Docker esté corriendo
docker ps

# Si no está, iniciarlo
docker start neo4j-twitterclone

# Ver logs
docker logs neo4j-twitterclone
```

### ❌ Error: "Authentication failed" (Neo4j)
Verifica que `.env` tenga las credenciales correctas:
```env
NEO4J_PASSWORD=password123  # Debe coincidir con Docker
```

### ❌ Puerto 8000 ya en uso
```bash
# Usar otro puerto
python manage.py runserver 8080

# O matar el proceso en 8000
lsof -ti:8000 | xargs kill -9
```

## 🎯 Primeros Pasos en la Aplicación

1. **Registra una cuenta** o inicia sesión con el superusuario
2. **Crea tu primer post** con hashtags (ej: "Hola #mundo #neo4j")
3. **Visita /interests/** para ver tus intereses
4. **Visita /analytics/** para ver análisis de red
5. **Busca otros usuarios** y agrégalos como amigos

## 📱 Funcionalidades Principales

### Crear Post con Hashtags
```
Mi primer post en #TwitterClone usando #Neo4j 🚀
```
Los hashtags se extraen automáticamente y se crean como InterestNodes.

### Agregar Amigos
1. Busca un usuario
2. Visita su perfil
3. Click en "Agregar Amigo"

### Ver Análisis
1. Ve a **/analytics/**
2. Verás:
   - Tus estadísticas
   - Amigos sugeridos
   - Usuarios para seguir
   - Influencers
   - Trending topics

## 🔄 Reiniciar Todo (Reset Completo)

```bash
# Detener servidor (Ctrl+C)

# Limpiar bases de datos
rm db.sqlite3
docker stop neo4j-twitterclone
docker rm neo4j-twitterclone

# Reiniciar Neo4j
docker run --name neo4j-twitterclone -p 7474:7474 -p 7687:7687 \
    -d -e NEO4J_AUTH=neo4j/password123 neo4j:5.14

# Re-migrar
python manage.py migrate
python manage.py createsuperuser
python manage.py create_dummy_data
python manage.py migrate_to_neo4j --clear

# Reiniciar servidor
python manage.py runserver
```

## 📚 Siguiente Nivel

Después de tener todo funcionando, explora:

1. **Neo4j Browser**: Ejecuta queries Cypher
   - Ver archivo: `CYPHER_QUERIES.md`

2. **Crear Relaciones**: Prueba agregar amigos y seguir usuarios

3. **Análisis Avanzado**: Experimenta con las sugerencias

4. **Documentación**: Lee los archivos:
   - `NEO4J_README.md` - Guía completa
   - `DATA_MODEL.md` - Modelo de datos
   - `DEPLOYMENT.md` - Despliegue en producción

## 💡 Tips Rápidos

- **Ver logs de Neo4j**: `docker logs -f neo4j-twitterclone`
- **Shell de Django**: `python manage.py shell`
- **Verificar rutas**: `python manage.py show_urls` (si tienes django-extensions)
- **Limpiar caché**: `python manage.py clear_cache`

## 🎓 Queries de Prueba en Neo4j

Abre http://localhost:7474 y prueba:

```cypher
// Ver todos los usuarios
MATCH (u:UserNode) RETURN u LIMIT 10

// Ver todas las relaciones
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 25

// Buscar posts con hashtag
MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode {name: 'neo4j'})
RETURN p

// Amigos en común
MATCH (me:UserNode {username: 'tu_usuario'})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(suggestion)
WHERE NOT (me)-[:FRIEND_OF]->(suggestion) AND me <> suggestion
RETURN suggestion.username, count(*) as common_friends
```

## ⏱️ Tiempo Total de Setup

- Neo4j con Docker: **2 min**
- Configurar proyecto: **3 min**
- Variables de entorno: **1 min**
- Migraciones: **2 min**
- Datos de prueba: **1 min**
- Iniciar servidor: **30 seg**

**Total: ~10 minutos** ⚡

---

## 🆘 ¿Algo no funciona?

1. Verifica que Docker esté corriendo: `docker ps`
2. Verifica la conexión a Neo4j: Query simple en http://localhost:7474
3. Revisa los logs: `docker logs neo4j-twitterclone`
4. Consulta documentación completa: `NEO4J_README.md`

## ✨ ¡Disfruta explorando tu Red Social con Neo4j!

**Happy coding! 🚀**
