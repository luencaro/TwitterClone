"""
Comando Django para migrar datos de SQLite a Neo4j
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment, Type, PostTag
from blog.neo4j_services import (
    Neo4jUserService, Neo4jPostService, Neo4jCommentService, 
    Neo4jInterestService
)
from blog.neo4j_connection import init_neo4j_connection


class Command(BaseCommand):
    help = 'Migra datos de SQLite a Neo4j'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpia la base de datos de Neo4j antes de migrar',
        )

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migración de datos a Neo4j...')
        
        # Inicializar conexión
        if not init_neo4j_connection():
            self.stdout.write(self.style.ERROR('Error al conectar con Neo4j'))
            return
        
        # Limpiar base de datos si se especificó
        if options['clear']:
            self.stdout.write('Limpiando base de datos de Neo4j...')
            self.clear_neo4j()
        
        # Migrar usuarios
        self.stdout.write('Migrando usuarios...')
        self.migrate_users()
        
        # Migrar posts
        self.stdout.write('Migrando publicaciones...')
        self.migrate_posts()
        
        # Migrar comentarios
        self.stdout.write('Migrando comentarios...')
        self.migrate_comments()
        
        # Migrar likes
        self.stdout.write('Migrando likes...')
        self.migrate_likes()
        
        self.stdout.write(self.style.SUCCESS('✓ Migración completada exitosamente'))

    def clear_neo4j(self):
        """Limpia todos los nodos y relaciones de Neo4j"""
        from neomodel import db
        try:
            db.cypher_query("MATCH (n) DETACH DELETE n")
            self.stdout.write(self.style.SUCCESS('✓ Base de datos limpiada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error limpiando base de datos: {e}'))

    def migrate_users(self):
        """Migra usuarios de Django a Neo4j"""
        user_service = Neo4jUserService()
        users = User.objects.all()
        
        for user in users:
            try:
                user_service.create_or_update_user(
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                self.stdout.write(f'  ✓ Usuario migrado: {user.username}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error migrando usuario {user.username}: {e}'))

    def migrate_posts(self):
        """Migra publicaciones de Django ORM a Neo4j"""
        post_service = Neo4jPostService()
        posts = Post.objects.all().select_related('username').prefetch_related('post_tags__type_id')
        
        for post in posts:
            try:
                post_service.create_post(
                    post_id=post.post_id,
                    user_id=post.username.id,
                    content=post.post_content
                )
                self.stdout.write(f'  ✓ Post migrado: {post.post_id}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error migrando post {post.post_id}: {e}'))

    def migrate_comments(self):
        """Migra comentarios de Django ORM a Neo4j"""
        comment_service = Neo4jCommentService()
        comments = Comment.objects.all().select_related('username', 'post_id')
        
        for comment in comments:
            try:
                comment_service.create_comment(
                    comment_id=comment.comment_id,
                    user_id=comment.username.id,
                    post_id=comment.post_id.post_id,
                    content=comment.comment_content
                )
                self.stdout.write(f'  ✓ Comentario migrado: {comment.comment_id}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error migrando comentario {comment.comment_id}: {e}'))

    def migrate_likes(self):
        """Migra likes de Django ORM a Neo4j"""
        post_service = Neo4jPostService()
        posts = Post.objects.all().prefetch_related('likes')
        
        total_likes = 0
        for post in posts:
            for user in post.likes.all():
                try:
                    post_service.like_post(user.id, post.post_id)
                    total_likes += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error migrando like: {e}'))
        
        self.stdout.write(f'  ✓ {total_likes} likes migrados')
