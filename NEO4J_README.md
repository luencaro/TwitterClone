# TwitterClone - Red Social con Neo4j

## 📋 Descripción

Esta es una aplicación web interactiva de red social desarrollada con Django que utiliza **Neo4j** como base de datos de grafos para gestionar eficientemente las relaciones entre usuarios, publicaciones, comentarios e intereses.

## 🌟 Características

### Gestión de Usuarios
- Creación de perfiles de usuario
- Autenticación y autorización
- Perfiles personalizables

### Red Social
- **Amigos**: Sistema de amistad bidireccional
- **Seguidores/Siguiendo**: Relaciones de seguimiento unidireccionales
- **Publicaciones**: Crear, editar y eliminar posts
- **Comentarios**: Interactuar en publicaciones
- **Likes**: Dar "me gusta" a publicaciones
- **Intereses/Hashtags**: Clasificar contenido por temas

### Análisis de Red (Powered by Neo4j)
- **Sugerencias de Amigos**: Basadas en amigos en común
- **Sugerencias de Usuarios**: Basadas en intereses comunes
- **Influencers**: Identificación de usuarios más seguidos
- **Intereses Trending**: Temas más populares
- **Intereses Comunes**: Entre amigos
- **Estadísticas de Red**: Análisis completo de conexiones

## 🛠️ Tecnologías

- **Backend**: Django 4.2.11
- **Base de Datos Relacional**: SQLite (para autenticación)
- **Base de Datos de Grafos**: Neo4j 5.x
- **OGM (Object-Graph Mapper)**: Neomodel 5.2.1
- **Driver de Neo4j**: neo4j 5.14.1
- **API REST**: Django REST Framework 3.14.0
- **Frontend**: Bootstrap 5, HTML5, JavaScript

## 📦 Instalación

### 1. Prerrequisitos

- Python 3.8+
- Neo4j 5.x instalado y corriendo
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

### 2. Instalación de Neo4j

#### En Ubuntu/Debian:
```bash
# Importar la clave GPG
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -

# Agregar repositorio
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Instalar
sudo apt-get update
sudo apt-get install neo4j

# Iniciar servicio
sudo systemctl start neo4j
sudo systemctl enable neo4j
```

#### Usando Docker:
```bash
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -d neo4j:5.14
```

### 3. Configuración del Proyecto

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd TwitterClone

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
```

### 4. Configurar Variables de Entorno

Edita el archivo `.env`:

```env
# Configuración de Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_password_aqui

# Django Secret Key
SECRET_KEY=tu_secret_key_aqui
```

### 5. Inicializar Base de Datos

```bash
# Migrar modelos de Django
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# (Opcional) Crear datos de prueba
python manage.py create_dummy_data

# Migrar datos a Neo4j
python manage.py migrate_to_neo4j --clear
```

### 6. Ejecutar el Servidor

```bash
python manage.py runserver
```

Visita: `http://localhost:8000`

## 🗂️ Estructura del Proyecto

```
TwitterClone/
├── blog/                           # App principal
│   ├── management/
│   │   └── commands/
│   │       ├── create_dummy_data.py    # Crear datos de prueba
│   │       └── migrate_to_neo4j.py     # Migrar datos a Neo4j
│   ├── neo4j_connection.py         # Conexión a Neo4j
│   ├── neo4j_models.py             # Modelos de nodos y relaciones
│   ├── neo4j_services.py           # Servicios de Neo4j
│   ├── social_views.py             # Vistas de red social
│   ├── models.py                   # Modelos Django (SQLite)
│   ├── views.py                    # Vistas principales
│   ├── urls.py                     # Rutas
│   ├── forms.py                    # Formularios
│   └── templates/                  # Templates HTML
│       └── blog/
│           ├── friends_list.html
│           ├── followers_list.html
│           ├── following_list.html
│           ├── interests_list.html
│           ├── network_analytics.html
│           └── user_profile_network.html
├── users/                          # App de usuarios
├── django_project/                 # Configuración Django
│   ├── settings.py
│   └── urls.py
├── requirements.txt                # Dependencias
├── .env.example                    # Ejemplo de variables de entorno
└── manage.py
```

## 📊 Modelo de Datos en Neo4j

### Nodos

1. **UserNode**
   - `user_id`: ID único del usuario
   - `username`: Nombre de usuario
   - `email`: Email
   - `first_name`, `last_name`: Nombres
   - `bio`: Biografía

2. **PostNode**
   - `post_id`: ID único del post
   - `content`: Contenido
   - `created_at`, `updated_at`: Fechas

3. **CommentNode**
   - `comment_id`: ID único
   - `content`: Contenido
   - `created_at`: Fecha

4. **InterestNode**
   - `name`: Nombre del interés/hashtag
   - `description`: Descripción
   - `created_at`: Fecha

### Relaciones

- `(:UserNode)-[:POSTED]->(:PostNode)` - Usuario crea post
- `(:UserNode)-[:COMMENTED]->(:CommentNode)` - Usuario crea comentario
- `(:CommentNode)-[:COMMENT_ON]->(:PostNode)` - Comentario en post
- `(:UserNode)-[:LIKES]->(:PostNode)` - Usuario da like a post
- `(:UserNode)-[:FOLLOWS]->(:UserNode)` - Usuario sigue a otro
- `(:UserNode)-[:FRIEND_OF]->(:UserNode)` - Amistad bidireccional
- `(:UserNode)-[:INTERESTED_IN]->(:InterestNode)` - Usuario interesado en tema
- `(:PostNode)-[:TAGGED_WITH]->(:InterestNode)` - Post etiquetado con hashtag

## 🔧 Comandos Útiles

### Comandos de Migración

```bash
# Migrar datos a Neo4j (limpiando datos anteriores)
python manage.py migrate_to_neo4j --clear

# Migrar sin limpiar
python manage.py migrate_to_neo4j
```

### Comandos de Neo4j

```bash
# Verificar conexión
python manage.py shell
>>> from blog.neo4j_connection import init_neo4j_connection
>>> init_neo4j_connection()
```

### Consultas Cypher Útiles

```cypher
// Ver todos los nodos
MATCH (n) RETURN n LIMIT 25;

// Ver todas las relaciones
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 25;

// Contar nodos por tipo
MATCH (n) RETURN labels(n), count(*);

// Encontrar usuarios más influyentes
MATCH (u:UserNode)<-[:FOLLOWS]-(f)
RETURN u.username, count(f) as followers
ORDER BY followers DESC
LIMIT 10;

// Encontrar amigos sugeridos para un usuario
MATCH (u:UserNode {username: 'tu_usuario'})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(suggestion)
WHERE NOT (u)-[:FRIEND_OF]->(suggestion) AND u <> suggestion
WITH suggestion, count(*) as common_friends
RETURN suggestion.username, common_friends
ORDER BY common_friends DESC;

// Intereses más populares
MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode)
WITH i, count(p) as post_count
RETURN i.name, post_count
ORDER BY post_count DESC
LIMIT 10;
```

## 🚀 Funcionalidades de la Aplicación

### Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal con feed de posts |
| `/friends/` | Lista de amigos |
| `/followers/` | Lista de seguidores |
| `/following/` | Lista de usuarios que sigo |
| `/interests/` | Gestión de intereses |
| `/interests/<nombre>/` | Posts por interés |
| `/analytics/` | Análisis de red y sugerencias |
| `/profile/<username>/` | Perfil de red de usuario |
| `/post/new/` | Crear nueva publicación |
| `/post/<id>/` | Detalle de publicación |

### API REST

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/l/users/` | GET | Lista de usuarios |
| `/l/groups/` | GET | Lista de grupos |
| `/api/posts` | GET | Lista de posts (API) |

## 🔐 Seguridad

- Autenticación requerida para todas las funciones de red social
- CSRF protection habilitado
- Validación de datos en formularios
- Contraseñas hasheadas con Django auth

## 🎨 Personalización

### Agregar Nuevas Relaciones

1. Definir en `neo4j_models.py`:
```python
class UserNode(StructuredNode):
    # ... propiedades existentes ...
    nueva_relacion = RelationshipTo('OtroNodo', 'TIPO_RELACION')
```

2. Crear servicio en `neo4j_services.py`:
```python
@staticmethod
def crear_nueva_relacion(user_id, otro_id):
    user = UserNode.nodes.get_or_none(user_id=user_id)
    otro = OtroNodo.nodes.get_or_none(id=otro_id)
    if user and otro:
        user.nueva_relacion.connect(otro)
        return True
    return False
```

3. Crear vista en `social_views.py` y agregar ruta en `urls.py`

## 📝 Notas Importantes

1. **Sistema Híbrido**: La aplicación usa SQLite para autenticación (Django User model) y Neo4j para relaciones sociales
2. **Sincronización**: Al crear usuarios en Django, ejecuta `migrate_to_neo4j` para sincronizar
3. **Performance**: Neo4j es especialmente eficiente para queries de grafos complejos
4. **Escalabilidad**: Para producción, considera usar PostgreSQL en lugar de SQLite

## 🐛 Troubleshooting

### Neo4j no se conecta
```bash
# Verificar que Neo4j esté corriendo
sudo systemctl status neo4j

# Ver logs
sudo journalctl -u neo4j -f

# Verificar puerto
netstat -tulpn | grep 7687
```

### Error de importación de neomodel
```bash
# Reinstalar dependencias
pip install --upgrade neomodel neo4j
```

### Datos no aparecen en Neo4j
```bash
# Re-migrar datos
python manage.py migrate_to_neo4j --clear
```

## 📚 Recursos

- [Documentación de Neo4j](https://neo4j.com/docs/)
- [Documentación de Neomodel](https://neomodel.readthedocs.io/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Cypher Query Language](https://neo4j.com/developer/cypher/)

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ✨ Autor

Desarrollado como proyecto educativo para aprendizaje de bases de datos de grafos con Neo4j.
