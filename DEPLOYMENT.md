# 🚀 Guía de Despliegue - TwitterClone con Neo4j

## Tabla de Contenidos
- [Requisitos Previos](#requisitos-previos)
- [Instalación de Neo4j](#instalación-de-neo4j)
- [Configuración del Proyecto](#configuración-del-proyecto)
- [Ejecución en Desarrollo](#ejecución-en-desarrollo)
- [Despliegue en Producción](#despliegue-en-producción)
- [Troubleshooting](#troubleshooting)

---

## 📋 Requisitos Previos

### Software Necesario
- **Python**: 3.8 o superior
- **Neo4j**: 5.x
- **pip**: Gestor de paquetes de Python
- **Git**: Para clonar el repositorio
- **Virtualenv** (opcional pero recomendado)

### Conocimientos Requeridos
- Comandos básicos de terminal
- Configuración de variables de entorno
- Conceptos básicos de bases de datos

---

## 🗄️ Instalación de Neo4j

### Opción 1: Docker (Recomendado para desarrollo)

```bash
# Descargar e iniciar Neo4j con Docker
docker run \
    --name neo4j-twitterclone \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/your_password \
    neo4j:5.14
```

#### Comandos útiles de Docker:
```bash
# Ver estado del contenedor
docker ps

# Ver logs
docker logs neo4j-twitterclone

# Detener
docker stop neo4j-twitterclone

# Iniciar
docker start neo4j-twitterclone

# Eliminar contenedor (¡CUIDADO! Se pierden los datos)
docker rm neo4j-twitterclone
```

### Opción 2: Instalación Nativa en Ubuntu/Debian

```bash
# 1. Importar la clave GPG de Neo4j
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -

# 2. Agregar el repositorio
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# 3. Actualizar paquetes
sudo apt-get update

# 4. Instalar Neo4j
sudo apt-get install neo4j

# 5. Iniciar el servicio
sudo systemctl start neo4j
sudo systemctl enable neo4j

# 6. Verificar estado
sudo systemctl status neo4j
```

#### Cambiar contraseña de Neo4j:
```bash
# Primera opción: Desde neo4j-admin
sudo neo4j-admin set-initial-password your_new_password

# Segunda opción: Desde el navegador
# Visita http://localhost:7474
# Usuario: neo4j
# Contraseña: neo4j (por defecto)
# Te pedirá cambiarla
```

### Opción 3: Neo4j Desktop (Para Windows/Mac)

1. Descargar Neo4j Desktop desde: https://neo4j.com/download/
2. Instalar y crear un nuevo proyecto
3. Crear una base de datos local
4. Establecer contraseña
5. Iniciar la base de datos

### Verificar Instalación

Accede al navegador de Neo4j:
- **URL**: http://localhost:7474
- **Usuario**: neo4j
- **Contraseña**: La que estableciste

---

## ⚙️ Configuración del Proyecto

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tuusuario/TwitterClone.git
cd TwitterClone
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar archivo .env
nano .env  # o usa tu editor preferido
```

Contenido del archivo `.env`:
```env
# Configuración de Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_password_aqui

# Django Secret Key (genera una nueva para producción)
SECRET_KEY=tu_secret_key_segura_aqui
```

**Generar SECRET_KEY segura:**
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Configurar Base de Datos Django

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 6. (Opcional) Crear Datos de Prueba

```bash
# Generar datos de prueba
python manage.py create_dummy_data

# Migrar datos a Neo4j
python manage.py migrate_to_neo4j --clear
```

---

## 🏃 Ejecución en Desarrollo

### Método Automático (Script)

```bash
# Dar permisos de ejecución
chmod +x setup.sh

# Ejecutar script de setup
./setup.sh
```

### Método Manual

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Verificar conexión a Neo4j
python -c "from blog.neo4j_connection import init_neo4j_connection; init_neo4j_connection()"

# 3. Iniciar servidor de desarrollo
python manage.py runserver

# 4. Acceder a la aplicación
# Navegador: http://localhost:8000
```

### URLs Importantes

- **Aplicación**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
- **Neo4j Browser**: http://localhost:7474
- **API REST**: http://localhost:8000/l/

---

## 🌐 Despliegue en Producción

### Preparación

1. **Cambiar DEBUG a False**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
   ```

2. **Usar PostgreSQL en lugar de SQLite**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'twitterclone_db',
           'USER': 'tu_usuario',
           'PASSWORD': 'tu_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Configurar archivos estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```

### Opción 1: Despliegue con Gunicorn + Nginx

#### 1. Instalar Gunicorn
```bash
pip install gunicorn
```

#### 2. Crear archivo de servicio systemd
```bash
sudo nano /etc/systemd/system/twitterclone.service
```

Contenido:
```ini
[Unit]
Description=TwitterClone Django Application
After=network.target

[Service]
User=tu_usuario
Group=www-data
WorkingDirectory=/ruta/a/TwitterClone
Environment="PATH=/ruta/a/TwitterClone/venv/bin"
ExecStart=/ruta/a/TwitterClone/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/ruta/a/TwitterClone/gunicorn.sock \
          django_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 3. Iniciar servicio
```bash
sudo systemctl start twitterclone
sudo systemctl enable twitterclone
```

#### 4. Configurar Nginx
```bash
sudo nano /etc/nginx/sites-available/twitterclone
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /ruta/a/TwitterClone;
    }

    location /media/ {
        root /ruta/a/TwitterClone;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/ruta/a/TwitterClone/gunicorn.sock;
    }
}
```

#### 5. Activar sitio
```bash
sudo ln -s /etc/nginx/sites-available/twitterclone /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Opción 2: Docker Compose

Crear `docker-compose.yml`:
```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.14
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/your_password
    volumes:
      - neo4j_data:/data

  web:
    build: .
    command: gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    depends_on:
      - neo4j
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=your_password

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  neo4j_data:
  static_volume:
```

### Configuración de Neo4j en Producción

1. **Aumentar memoria asignada**
   ```bash
   # Editar neo4j.conf
   sudo nano /etc/neo4j/neo4j.conf
   
   # Ajustar estos valores según tu servidor:
   dbms.memory.heap.initial_size=2G
   dbms.memory.heap.max_size=4G
   dbms.memory.pagecache.size=4G
   ```

2. **Habilitar backups**
   ```bash
   # Backup manual
   neo4j-admin backup --backup-dir=/path/to/backup --database=neo4j
   
   # Backup automático (cron)
   0 2 * * * /usr/bin/neo4j-admin backup --backup-dir=/backups/neo4j --database=neo4j
   ```

3. **Configurar autenticación robusta**
   ```bash
   # En producción, usar contraseñas fuertes
   # Considerar LDAP o autenticación externa
   ```

### Seguridad

1. **Firewall**
   ```bash
   # Permitir solo puertos necesarios
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 7687/tcp  # Solo si Neo4j está en servidor separado
   sudo ufw enable
   ```

2. **SSL/HTTPS con Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
   ```

3. **Variables de entorno seguras**
   - No commitear archivo `.env`
   - Usar servicios como AWS Secrets Manager
   - Rotar contraseñas regularmente

---

## 🔍 Troubleshooting

### Neo4j no inicia

```bash
# Ver logs
sudo journalctl -u neo4j -n 50

# Verificar configuración
sudo neo4j-admin check-config

# Verificar puertos
sudo netstat -tulpn | grep 7687
```

### Error de conexión Django-Neo4j

```python
# Verificar desde Python
python manage.py shell

>>> from blog.neo4j_connection import init_neo4j_connection
>>> init_neo4j_connection()
```

### Problema con dependencias

```bash
# Reinstalar todo
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Migración no funciona

```bash
# Limpiar y re-migrar
python manage.py migrate_to_neo4j --clear

# Verificar datos en Neo4j Browser
# MATCH (n) RETURN n LIMIT 25
```

### Performance lenta

```cypher
-- Crear índices en Neo4j Browser
CREATE INDEX user_username IF NOT EXISTS FOR (u:UserNode) ON (u.username);
CREATE INDEX user_id IF NOT EXISTS FOR (u:UserNode) ON (u.user_id);
CREATE INDEX post_id IF NOT EXISTS FOR (p:PostNode) ON (p.post_id);
```

---

## 📊 Monitoreo

### Logs de Django
```bash
# Ver logs en tiempo real
tail -f /var/log/twitterclone/django.log
```

### Logs de Neo4j
```bash
# Ver logs
sudo tail -f /var/log/neo4j/neo4j.log

# Query log
sudo tail -f /var/log/neo4j/query.log
```

### Métricas de Neo4j
```cypher
-- En Neo4j Browser
CALL dbms.queryJmx("org.neo4j:instance=kernel#0,name=Transactions")
YIELD attributes
RETURN attributes;
```

---

## 🔄 Actualización

```bash
# 1. Hacer backup
python manage.py dumpdata > backup.json

# 2. Pull cambios
git pull origin main

# 3. Actualizar dependencias
pip install -r requirements.txt --upgrade

# 4. Aplicar migraciones
python manage.py migrate

# 5. Colectar estáticos
python manage.py collectstatic --noinput

# 6. Reiniciar servicios
sudo systemctl restart twitterclone
```

---

## 📞 Soporte

Para problemas o preguntas:
- Revisar documentación de Django: https://docs.djangoproject.com/
- Revisar documentación de Neo4j: https://neo4j.com/docs/
- Crear issue en el repositorio

---

**¡Tu aplicación TwitterClone con Neo4j está lista para despegar! 🚀**
