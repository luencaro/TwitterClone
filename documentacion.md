# TwitterClone_BBDD

Aplicación web construida con Django que replica las características esenciales de Twitter: publicación de mensajes cortos, sistema de comentarios, hashtags, likes en tiempo real sin recargar la página y gestión de perfiles de usuario. El proyecto se desarrolló para la asignatura de Bases de Datos y sirve como base para practicar autenticación, CRUD completos y consumo de una API REST interna.

## Tabla de contenido

- [TwitterClone\_BBDD](#twitterclone_bbdd)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Características principales](#características-principales)
  - [Arquitectura y estructura de carpetas](#arquitectura-y-estructura-de-carpetas)
  - [Requisitos previos](#requisitos-previos)
  - [Instalación y puesta en marcha](#instalación-y-puesta-en-marcha)
  - [Uso de la aplicación](#uso-de-la-aplicación)
    - [Autenticación y perfiles](#autenticación-y-perfiles)
    - [Publicaciones y hashtags](#publicaciones-y-hashtags)
    - [Comentarios y likes](#comentarios-y-likes)
    - [Búsquedas](#búsquedas)
  - [API REST integrada](#api-rest-integrada)
  - [Gestión de datos de ejemplo](#gestión-de-datos-de-ejemplo)
  - [Ejecución de pruebas](#ejecución-de-pruebas)
  - [Buenas prácticas y seguridad](#buenas-prácticas-y-seguridad)
  - [Licencia](#licencia)

## Características principales

- **Autenticación completa**: registro, login/logout, restablecimiento y cambio de contraseña, búsqueda de usuarios y eliminación definitiva de cuenta.
- **CRUD de contenidos**:
  - Usuarios: alta, edición (incluye cambio de contraseña) y eliminación.
  - Posts: creación, edición, borrado y listado por usuario.
  - Comentarios: los autores pueden editar y eliminar sus propias respuestas.
- **Likes dinámicos**: botón de “Me gusta” que utiliza `fetch` para actualizar el contador sin recargar la página.
- **Hashtags**: detección automática en el contenido del post, creación de etiquetas y filtrado por hashtag o búsqueda libre.
- **Diseño responsive**: experiencia cuidada tanto en escritorio como en dispositivos móviles.
- **API REST** (Django REST Framework) para usuarios, grupos y posts.
- **Gestión de archivos estáticos y multimedia**: incluye soporte para imágenes de perfil y recursos de Bootstrap.

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

## Gestión de datos de ejemplo

Existe un comando personalizado para poblar la base de datos con posts de prueba:

```powershell
python manage.py create_dummy_data
```

Puedes modificar el comando en `blog/management/commands/create_dummy_data.py` para ajustar la cantidad de entradas.

## Ejecución de pruebas

La suite de tests básicos se ejecuta con:

```powershell
python manage.py test
```

El comando crea una base de datos temporal, verifica modelos y vistas fundamentales, y luego limpia los datos.

## Buenas prácticas y seguridad

- Mantén actualizado el archivo `requirements.txt` y aplica parches de seguridad.
- Si despliegas en producción, configura variables de entorno (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) y ejecuta `python manage.py collectstatic`.
- Usa HTTPS en producción y un backend de correo real para la recuperación de contraseñas.
- Revisa los permisos de archivos subidos en `media/` y configura un almacenamiento apropiado (S3, Azure Blob, etc.).

## Licencia

Este proyecto se distribuye conforme a la licencia incluida en el archivo `LICENSE`.
