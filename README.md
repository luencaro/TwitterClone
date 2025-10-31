# TwitterClone - Red Social con Neo4j

[![Django](https://img.shields.io/badge/Django-4.2.11-green.svg)](https://www.djangoproject.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.14-blue.svg)](https://neo4j.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

Aplicación web de red social desarrollada con Django que utiliza **Neo4j** como base de datos de grafos para modelar eficientemente las relaciones entre usuarios, publicaciones, comentarios e intereses.

## 🌟 Características Principales

### Funcionalidades Core
- ✅ Sistema de autenticación y registro
- ✅ Creación y gestión de publicaciones
- ✅ Sistema de comentarios
- ✅ Likes en publicaciones
- ✅ Hashtags y categorización

### Red Social con Neo4j
- 🤝 **Sistema de Amigos**: Relaciones bidireccionales
- 👥 **Seguimiento**: Follow/Unfollow de usuarios
- 🏷️ **Intereses**: Seguimiento de temas/hashtags
- 📊 **Feed Personalizado**: Posts de usuarios seguidos

### Análisis Inteligente
- 🔍 **Sugerencias de Amigos**: Basadas en amigos en común
- 💡 **Recomendaciones**: Usuarios con intereses similares
- 🌟 **Identificación de Influencers**: Rankings de usuarios
- 📈 **Trending Topics**: Temas más populares
- 📉 **Análisis de Red**: Estadísticas completas

## ⚡ Inicio Rápido

### Instalación Automática
```bash
chmod +x setup.sh
./setup.sh
```

### Instalación Manual
```bash
# 1. Iniciar Neo4j
docker run --name neo4j -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password -d neo4j:5.14

# 2. Configurar proyecto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Migrar datos
python manage.py migrate
python manage.py createsuperuser
python manage.py migrate_to_neo4j --clear

# 5. Iniciar servidor
python manage.py runserver
```

**Visita:** http://localhost:8000

## 🚀 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje principal |
| Django | 4.2.11 | Framework web |
| **Neo4j** | **5.14+** | **Base de datos de grafos** |
| **Neomodel** | **5.2.1** | **OGM para Neo4j** |
| SQLite | - | Auth y sesiones |
| Bootstrap | 5 | Frontend |
| REST Framework | 3.14.0 | API REST |

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│           TwitterClone Application          │
├─────────────────────────────────────────────┤
│  ┌──────────────┐      ┌──────────────┐     │
│  │   Django     │◄────►│    Neo4j     │     │
│  │  (SQLite)    │      │   (Grafos)   │     │
│  └──────────────┘      └──────────────┘     │
│        │                       │            │
│  ┌─────▼──────┐      ┌────────▼────────┐    │
│  │ User Auth  │      │  Social Graph   │    │
│  │ Sessions   │      │  Relationships  │    │
│  └────────────┘      └─────────────────┘    │
└─────────────────────────────────────────────┘
```

## �️ Estructura del Proyecto

El proyecto incluye un diseño detallado de la base de datos y scripts para su creación:

1.  **Diagrama Entidad-Relación (ERD):** Visualización de las entidades principales (Usuarios, Posts, Comentarios, Tipos de Post) y sus relaciones.
2.  **Modelo Relacional:** Especificación de tablas, atributos, tipos de datos, claves primarias y foráneas, y restricciones de integridad.
3.  **Script SQL:** Un script para la creación de las tablas de la base de datos.

## 💡 Funcionalidades de la Aplicación

La aplicación ofrece un menú interactivo con las siguientes funcionalidades principales:

*   **Operaciones CRUD para Usuarios:** Crear, ver, actualizar y eliminar usuarios.
*   **Operaciones CRUD para Posts:** Crear, ver, actualizar y eliminar posts (con eliminación en cascada de comentarios).
*   **Operaciones CRUD para Comentarios:** Añadir, ver, actualizar y eliminar comentarios.
*   **Operaciones CRUD para Tipos de Posts:** Crear, ver, actualizar y eliminar tipos de post.
*   **Búsqueda de Posts:** Buscar posts por tipo, tema, autor y palabras clave.
*   **Visualización de Posts Completos:** Ver el contenido completo de un post y todos sus comentarios asociados.
*   **Listado de Usuarios y Cantidad de Posts:** Un listado que muestra cada usuario y el número total de posts que ha publicado.


### Restricciones Implementadas

*   Un post solo puede ser editado o eliminado por su autor.
*   Un comentario solo puede ser editado o eliminado por su autor.

## 🤝 Integrantes del Grupo

*   Juan Aguirre
*   Luis Cabarcas
*   Andres España
*   Jose Menco
*   Camilo Vargas


## Arquitectura y estructura de carpetas

```
Project/
├── blog/               # App principal (posts, comentarios, likes, hashtags)
│   ├── management/     # Comandos custom (p. ej. carga de datos dummy)
│   ├── templates/      # Vistas HTML (home, detalle, formularios, etc.)
│   ├── static/blog/    # CSS, JS (likes.js) e imágenes
│   └── serializers.py  # Exposición de entidades vía DRF
├── users/              # App para perfiles, registro y autenticación adicional
│   ├── templates/users/ # Formularios de registro, login, perfil, cambio de contraseña
│   └── forms.py         # Formularios personalizados (registro/edición)
├── django_project/     # Configuración global de Django (settings, urls)
├── media/              # Archivos subidos por los usuarios
├── staticfiles/        # Carpeta generada por `collectstatic`
├── requirements.txt    # Dependencias del proyecto
└── manage.py           # Punto de entrada de Django
```

## Requisitos previos

- Python 3.10 o superior
- Pip y `venv` habilitados
- SQLite (incluida por defecto con Python)
- (Opcional) Node/npm si se desea gestionar assets adicionales

## Instalación y puesta en marcha

1. **Clonar el repositorio**

    ```bash
    git clone https://github.com/LasciaStare/TwitterClone_BBDD.git
    cd TwitterClone_BBDD/Project
    ```

2. **Crear y activar entorno virtual** (PowerShell en Windows)

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```

3. **Instalar dependencias**

    ```powershell
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Aplicar migraciones**

    ```powershell
    python manage.py migrate
    ```

5. **Crear superusuario (opcional pero recomendado)**

    ```powershell
    python manage.py createsuperuser
    ```

6. **Ejecutar el servidor de desarrollo**

    ```powershell
    python manage.py runserver
    ```

    Visita <http://127.0.0.1:8000/> en tu navegador y autentícate para acceder al feed.

## Uso de la aplicación

### Autenticación y perfiles
- Registro mediante formulario (`/register/`).
- Login (`/login/`) y logout (`/logout/`).
- Búsqueda de usuarios desde la barra de búsqueda interna.
- Página “Mi perfil” para actualizar nombre de usuario, email, cambiar contraseña y eliminar la cuenta definitivamente.

### Publicaciones y hashtags
- Crea publicaciones con el botón “Nuevo post”.
- Los hashtags se detectan automáticamente y permiten filtrar el feed (`/?type=hashtag`).
- Las publicaciones pueden editarse o borrarse por sus autores.

### Comentarios y likes
- Los comentarios se gestionan desde la página de detalle de cada post.
- El botón de “Me gusta” funciona sin recargar la página gracias a `likes.js`; si el usuario no ha iniciado sesión, se redirige al login.

### Búsquedas
- El campo superior realiza búsquedas tanto por hashtag (con o sin `#`) como por texto libre en contenido y usuarios.

## API REST integrada

La aplicación expone endpoints básicos mediante Django REST Framework:

- `GET /l/users/` – listado de usuarios autenticado
- `GET /l/groups/` – listado de grupos
- `GET | POST | DELETE /api/posts` – listado, creación y eliminación masiva de posts (requiere autenticación)

Para interactuar con la API, autentícate mediante la sesión de Django o usa tokens si añades un backend adicional.



## 🗓️ Fecha del Laboratorio
31 de Octubre de 2025

---
