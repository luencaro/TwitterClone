#!/usr/bin/env python
"""
Script para crear datos de demostración con múltiples usuarios,
posts, comentarios, likes y relaciones de seguimiento.
"""
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment
from blog.neo4j_services import Neo4jUserService, Neo4jPostService, Neo4jCommentService

# Datos de usuarios
USERS_DATA = [
    {
        'username': 'maria_dev',
        'email': 'maria@example.com',
        'first_name': 'María',
        'last_name': 'García',
        'password': 'demo123'
    },
    {
        'username': 'carlos_tech',
        'email': 'carlos@example.com',
        'first_name': 'Carlos',
        'last_name': 'López',
        'password': 'demo123'
    },
    {
        'username': 'ana_design',
        'email': 'ana@example.com',
        'first_name': 'Ana',
        'last_name': 'Martínez',
        'password': 'demo123'
    },
    {
        'username': 'luis_data',
        'email': 'luis@example.com',
        'first_name': 'Luis',
        'last_name': 'Rodríguez',
        'password': 'demo123'
    },
    {
        'username': 'sofia_code',
        'email': 'sofia@example.com',
        'first_name': 'Sofía',
        'last_name': 'Hernández',
        'password': 'demo123'
    },
]

# Posts por usuario (username: [posts])
POSTS_DATA = {
    'admin': [
        "¡Explorando #neo4j para el proyecto final! 🚀 #database #graphdb",
        "Mi experiencia con #django después de 6 meses #python #webdev",
        "Tutorial: Cómo integrar #neo4j con #django #tutorial",
        "Comparando bases de datos relacionales vs grafos #database #neo4j",
    ],
    'maria_dev': [
        "Aprendiendo #react hoy, ¡me encanta! 💙 #javascript #frontend",
        "Mi primer proyecto full-stack con #django y #react #webdev",
        "#javascript ES6+ es increíble para desarrollo moderno",
        "Tips para principiantes en #react #frontend #webdev",
        "Integrando APIs REST con #django y #react #fullstack",
    ],
    'carlos_tech': [
        "Backend con #python y #django = ❤️ #webdev",
        "Optimizando queries en #neo4j para mejor performance #database",
        "¿Por qué elegir #django sobre otros frameworks? #python",
        "#graphdb revoluciona cómo pensamos sobre relaciones #neo4j",
        "Machine Learning con #python y #tensorflow #ai #ml",
    ],
    'ana_design': [
        "Diseño de interfaces con #react y #tailwindcss 🎨 #frontend #design",
        "UX/UI tips para desarrolladores #design #webdev",
        "Componentes reutilizables en #react #javascript",
        "Animaciones suaves con #css y #javascript #frontend",
    ],
    'luis_data': [
        "Análisis de datos con #python y #pandas #datascience",
        "Visualizaciones increíbles con #matplotlib #python #datavis",
        "#neo4j para análisis de redes sociales #graphdb #datascience",
        "ETL pipelines con #python #dataengineering",
        "Big Data y #database #neo4j #python",
    ],
    'sofia_code': [
        "100 días de código con #python 💪 #100daysofcode",
        "Algoritmos y estructuras de datos en #python #coding",
        "Proyectos personales con #django #webdev",
        "Contribuyendo a open source #opensource #python",
        "Clean code principles #cleancode #python #bestpractices",
    ],
}

# Comentarios (aleatorios)
COMMENTS_TEMPLATES = [
    "¡Excelente post! 👏",
    "Muy interesante, gracias por compartir",
    "¿Podrías compartir más detalles?",
    "Me ayudó mucho, gracias! 🙏",
    "Totalmente de acuerdo",
    "Gran contenido como siempre",
    "Esto es justo lo que necesitaba",
    "¿Tienes algún tutorial sobre esto?",
    "Impresionante trabajo! 🚀",
    "Aprendí algo nuevo hoy",
]

def create_users():
    """Crear usuarios de demostración"""
    print("\n👥 CREANDO USUARIOS")
    print("=" * 50)
    
    created_users = []
    user_service = Neo4jUserService()
    
    for user_data in USERS_DATA:
        # Crear en Django
        try:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f"✅ Usuario Django: {user.username}")
            
            # Sincronizar con Neo4j
            user_service.create_or_update_user(
                user.id, user.username, user.email,
                user.first_name, user.last_name
            )
            print(f"   └─ Neo4j: {user.username}")
            
            created_users.append(user)
        except Exception as e:
            print(f"⚠️  Usuario {user_data['username']} ya existe o error: {e}")
            user = User.objects.get(username=user_data['username'])
            created_users.append(user)
    
    return created_users

def create_posts(users):
    """Crear posts para cada usuario"""
    print("\n📝 CREANDO POSTS")
    print("=" * 50)
    
    all_posts = []
    post_service = Neo4jPostService()
    
    for user in users:
        username = user.username
        if username not in POSTS_DATA:
            continue
            
        posts_content = POSTS_DATA[username]
        
        for content in posts_content:
            # Crear en Django
            post = Post.objects.create(
                username=user,
                post_content=content
            )
            print(f"✅ Post [{post.post_id}] {username}: {content[:50]}...")
            
            # Sincronizar con Neo4j
            post_service.create_post(
                post_id=post.post_id,
                user_id=user.id,
                content=content
            )
            
            all_posts.append(post)
    
    return all_posts

def create_comments(users, posts):
    """Crear comentarios aleatorios en posts"""
    print("\n💬 CREANDO COMENTARIOS")
    print("=" * 50)
    
    comment_service = Neo4jCommentService()
    num_comments = min(30, len(posts) * 2)  # 2 comentarios por post aprox
    
    for _ in range(num_comments):
        # Seleccionar post y usuario aleatorio
        post = random.choice(posts)
        user = random.choice(users)
        
        # Evitar auto-comentarios (a veces)
        if user.id == post.username.id and random.random() < 0.7:
            continue
        
        comment_text = random.choice(COMMENTS_TEMPLATES)
        
        # Crear en Django
        comment = Comment.objects.create(
            username=user,
            post_id=post,
            comment_content=comment_text
        )
        print(f"✅ Comentario: {user.username} → Post {post.post_id}")
        
        # Sincronizar con Neo4j
        comment_service.create_comment(
            comment_id=comment.comment_id,
            user_id=user.id,
            post_id=post.post_id,
            content=comment_text
        )

def create_follows(users):
    """Crear relaciones de seguimiento entre usuarios"""
    print("\n👥 CREANDO RELACIONES DE SEGUIMIENTO")
    print("=" * 50)
    
    user_service = Neo4jUserService()
    
    # Cada usuario sigue a algunos otros aleatoriamente
    for user in users:
        # Determinar cuántos usuarios seguir (entre 2 y 4)
        num_to_follow = random.randint(2, min(4, len(users) - 1))
        
        # Seleccionar usuarios aleatorios para seguir (excepto a sí mismo)
        other_users = [u for u in users if u.id != user.id]
        to_follow = random.sample(other_users, num_to_follow)
        
        for followed_user in to_follow:
            try:
                user_service.follow_user(user.id, followed_user.id)
                print(f"✅ {user.username} → sigue a → {followed_user.username}")
            except Exception as e:
                print(f"⚠️  Error: {e}")

def create_likes(users, posts):
    """Crear likes aleatorios en posts"""
    print("\n❤️  CREANDO LIKES")
    print("=" * 50)
    
    num_likes = min(50, len(posts) * 3)  # 3 likes por post aprox
    
    for _ in range(num_likes):
        post = random.choice(posts)
        user = random.choice(users)
        
        # Agregar like (Django maneja duplicados automáticamente)
        post.likes.add(user)
    
    print(f"✅ {num_likes} likes creados")

def show_statistics():
    """Mostrar estadísticas finales"""
    print("\n📊 ESTADÍSTICAS FINALES")
    print("=" * 50)
    
    print(f"👥 Usuarios: {User.objects.count()}")
    print(f"📝 Posts: {Post.objects.count()}")
    print(f"💬 Comentarios: {Comment.objects.count()}")
    
    # Trending hashtags
    from blog.neo4j_services import Neo4jAnalyticsService
    analytics = Neo4jAnalyticsService()
    trending = analytics.get_trending_interests(limit=10)
    
    print(f"\n🔥 Top 10 Trending Hashtags:")
    for item in trending:
        print(f"   #{item['interest'].name}: {item['count']} posts")
    
    print("\n🔐 CREDENCIALES DE USUARIOS:")
    print("=" * 50)
    print("   admin / admin123")
    for user_data in USERS_DATA:
        print(f"   {user_data['username']} / {user_data['password']}")

def main():
    print("🚀 CREANDO DATOS DE DEMOSTRACIÓN")
    print("=" * 50)
    
    # Crear usuarios
    users = create_users()
    
    # Obtener admin si existe
    try:
        admin = User.objects.get(username='admin')
        if admin not in users:
            users.insert(0, admin)
    except User.DoesNotExist:
        print("⚠️  Usuario admin no encontrado")
    
    # Crear posts
    posts = create_posts(users)
    
    # Crear comentarios
    create_comments(users, posts)
    
    # Crear follows
    create_follows(users)
    
    # Crear likes
    create_likes(users, posts)
    
    # Mostrar estadísticas
    show_statistics()
    
    print("\n✅ ¡DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE!")
    print("\n🚀 Inicia el servidor con: python manage.py runserver")

if __name__ == '__main__':
    main()
