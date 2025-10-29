#!/bin/bash

echo "🔄 RESET COMPLETO DE LA BASE DE DATOS"
echo "======================================"
echo ""
echo "⚠️  ADVERTENCIA: Esto eliminará TODOS los datos"
echo "   - SQLite (Django): db.sqlite3"
echo "   - Neo4j: Todos los nodos y relaciones"
echo ""
read -p "¿Estás seguro? (escribe 'SI' para continuar): " confirmacion

if [ "$confirmacion" != "SI" ]; then
    echo "❌ Operación cancelada"
    exit 1
fi

echo ""
echo "📋 Paso 1: Eliminando base de datos SQLite..."
rm -f db.sqlite3
echo "✅ db.sqlite3 eliminado"

echo ""
echo "📋 Paso 2: Limpiando Neo4j..."
python manage.py shell -c "
from blog import neo4j_connection
from neomodel import db

# Eliminar todos los nodos y relaciones
query = 'MATCH (n) DETACH DELETE n'
db.cypher_query(query)
print('✅ Neo4j limpiado - todos los nodos eliminados')
"

echo ""
echo "📋 Paso 3: Recreando estructura de base de datos Django..."
python manage.py migrate
echo "✅ Migraciones aplicadas"

echo ""
echo "📋 Paso 4: Creando superusuario..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell
echo "✅ Superusuario creado: admin / admin123"

echo ""
echo "📋 Paso 5: Creando usuarios de prueba..."
python manage.py shell -c "
from django.contrib.auth.models import User
from users.models import Profile

users_data = [
    ('maria_tech', 'maria@example.com', 'María', 'García'),
    ('carlos_dev', 'carlos@example.com', 'Carlos', 'López'),
    ('ana_design', 'ana@example.com', 'Ana', 'Martínez'),
]

for username, email, first_name, last_name in users_data:
    user = User.objects.create_user(
        username=username,
        email=email,
        password='testpass123',
        first_name=first_name,
        last_name=last_name
    )
    # El profile se crea automáticamente por la señal
    print(f'✅ Usuario creado: {username}')

print(f'✅ Total usuarios: {User.objects.count()}')
"

echo ""
echo "📋 Paso 6: Creando posts de ejemplo con hashtags..."
python manage.py shell -c "
from django.contrib.auth.models import User
from blog.models import Post
from blog.neo4j_services import Neo4jPostService, Neo4jUserService

# Posts de ejemplo con diferentes hashtags
posts_data = [
    ('admin', 'Iniciando con #django y #python 🚀'),
    ('admin', 'Mi primer proyecto usando #neo4j para analíticas'),
    ('maria_tech', 'Aprendiendo #javascript y #react hoy'),
    ('maria_tech', 'Tutorial de #python para principiantes #django'),
    ('carlos_dev', 'Comparando #django vs #flask #python'),
    ('carlos_dev', 'Base de datos #neo4j es perfecta para redes sociales #database'),
    ('ana_design', 'Diseñando UI con #react y #javascript'),
    ('ana_design', 'Mi experiencia con #django templates'),
    ('admin', 'Proyecto final: #django + #neo4j + #python'),
    ('maria_tech', '#javascript es increíble para frontend'),
    ('carlos_dev', 'Backend con #python y #django'),
    ('ana_design', 'Full stack: #react + #django + #neo4j'),
]

for username, content in posts_data:
    user = User.objects.get(username=username)
    
    # Crear post en Django
    post = Post.objects.create(
        username=user,
        post_content=content
    )
    
    # Sincronizar con Neo4j
    try:
        user_service = Neo4jUserService()
        user_service.create_or_update_user(
            user.id, user.username, user.email,
            user.first_name, user.last_name
        )
        
        post_service = Neo4jPostService()
        post_service.create_post(
            post_id=post.post_id,
            user_id=user.id,
            content=content
        )
        print(f'✅ [{post.post_id}] {username}: {content[:50]}...')
    except Exception as e:
        print(f'❌ Error en post {post.post_id}: {e}')

print(f'\\n✅ Total posts creados: {Post.objects.count()}')
"

echo ""
echo "📋 Paso 7: Creando algunas relaciones de follow..."
python manage.py shell -c "
from django.contrib.auth.models import User
from blog.neo4j_services import Neo4jUserService

# Crear algunas relaciones de seguimiento
follows = [
    ('maria_tech', 'admin'),
    ('carlos_dev', 'admin'),
    ('ana_design', 'admin'),
    ('admin', 'maria_tech'),
    ('admin', 'carlos_dev'),
    ('maria_tech', 'carlos_dev'),
]

user_service = Neo4jUserService()

for follower_username, followed_username in follows:
    follower = User.objects.get(username=follower_username)
    followed = User.objects.get(username=followed_username)
    
    try:
        user_service.follow_user(follower.id, followed.id)
        print(f'✅ {follower_username} → {followed_username}')
    except Exception as e:
        print(f'❌ Error: {e}')
"

echo ""
echo "📋 Paso 8: Verificando conteo de hashtags..."
python manage.py shell -c "
from blog.neo4j_services import Neo4jAnalyticsService

analytics = Neo4jAnalyticsService()
trending = analytics.get_trending_interests(limit=10)

print('\\n🔥 Trending Hashtags:')
print('=' * 40)
for item in trending:
    print(f\"  #{item['interest'].name}: {item['count']} posts\")
print('=' * 40)
"

echo ""
echo "✅ ¡RESET COMPLETADO!"
echo ""
echo "📊 Resumen:"
echo "   - Base de datos SQLite: Nueva"
echo "   - Neo4j: Limpio y sincronizado"
echo "   - Usuarios: 4 (admin + 3 usuarios de prueba)"
echo "   - Posts: 12 con diferentes hashtags"
echo "   - Relaciones: Algunos follows entre usuarios"
echo ""
echo "🔐 Credenciales:"
echo "   Usuario: admin"
echo "   Password: admin123"
echo ""
echo "🚀 Inicia el servidor con: python manage.py runserver"
