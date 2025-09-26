from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Type, Comment, PostTag
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Crear datos dummy para la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Número de usuarios a crear (default: 10)'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=50,
            help='Número de posts a crear (default: 50)'
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=100,
            help='Número de comentarios a crear (default: 100)'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_posts = options['posts']
        num_comments = options['comments']

        self.stdout.write('Creando datos dummy...')

        # Crear usuarios
        self.stdout.write('Creando usuarios...')
        users_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'first_name': 'Admin', 'last_name': 'User'},
            {'username': 'jose_dev', 'email': 'jose@example.com', 'first_name': 'José', 'last_name': 'Developer'},
            {'username': 'maria_tech', 'email': 'maria@example.com', 'first_name': 'María', 'last_name': 'Tech'},
            {'username': 'carlos_code', 'email': 'carlos@example.com', 'first_name': 'Carlos', 'last_name': 'Coder'},
            {'username': 'ana_design', 'email': 'ana@example.com', 'first_name': 'Ana', 'last_name': 'Designer'},
            {'username': 'luis_data', 'email': 'luis@example.com', 'first_name': 'Luis', 'last_name': 'DataSci'},
            {'username': 'sofia_ui', 'email': 'sofia@example.com', 'first_name': 'Sofía', 'last_name': 'UX'},
            {'username': 'diego_back', 'email': 'diego@example.com', 'first_name': 'Diego', 'last_name': 'Backend'},
            {'username': 'laura_front', 'email': 'laura@example.com', 'first_name': 'Laura', 'last_name': 'Frontend'},
            {'username': 'pedro_full', 'email': 'pedro@example.com', 'first_name': 'Pedro', 'last_name': 'Fullstack'},
        ]

        created_users = []
        for i, user_data in enumerate(users_data):
            if i >= num_users:
                break
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Usuario creado: {user.username}')
            else:
                self.stdout.write(f'Usuario ya existe: {user.username}')
            created_users.append(user)

        # Crear tipos/categorías
        self.stdout.write('Creando tipos/categorías...')
        types_data = [
            'Tecnología',
            'Programación',
            'Django',
            'Python',
            'JavaScript',
            'React',
            'Vue.js',
            'Node.js',
            'Bases de Datos',
            'DevOps',
            'Machine Learning',
            'Diseño',
            'UX/UI',
            'Móvil',
            'Web',
        ]

        created_types = []
        for type_name in types_data:
            type_obj, created = Type.objects.get_or_create(type_name=type_name)
            if created:
                self.stdout.write(f'Tipo creado: {type_name}')
            created_types.append(type_obj)

        # Crear posts
        self.stdout.write('Creando posts...')
        posts_content = [
            "¡Acabo de terminar mi primer proyecto en Django! 🎉 #Django #Python",
            "¿Alguien más está emocionado por las nuevas características de Python 3.12? 🐍",
            "Trabajando en una nueva API REST con Django REST Framework. Las vistas basadas en clases son geniales!",
            "Tip del día: Siempre usa entornos virtuales para tus proyectos de Python 📦",
            "¿Cuál es vuestra librería favorita de JavaScript? Yo estoy entre React y Vue.js 🤔",
            "Implementando autenticación JWT en mi app. La seguridad es clave! 🔐",
            "¿Alguien ha probado FastAPI? Parece muy prometedor para APIs rápidas ⚡",
            "CSS Grid vs Flexbox: ¿Cuál prefieres para layouts? 🎨",
            "Acabé de deployar mi app en Heroku. ¡Qué fácil es ahora! ☁️",
            "Docker está revolucionando mi workflow de desarrollo 🐳",
            "¿Consejos para optimizar queries de Django ORM? 🔍",
            "Machine Learning con Python: scikit-learn es increíble 🤖",
            "Diseñando una nueva interfaz de usuario. UX primero siempre! 💡",
            "GraphQL vs REST API: ¿Cuál elegirías para tu próximo proyecto? 🔄",
            "Aprendiendo TypeScript y me está encantando la tipificación estática ✨",
            "¿Alguien más está obsesionado con la performance web? 🚀",
            "Implementando tests unitarios. El código sin tests es código roto 🧪",
            "Vue 3 Composition API es genial para componentes complejos 💚",
            "Trabajando con websockets en Django Channels. Real-time is the future! ⚡",
            "¿Mejores prácticas para estructurar un proyecto Django grande? 🏗️",
            "Redis para caching: game changer para la performance 🏎️",
            "Microservicios vs Monolitos: depende del contexto 🏢",
            "Automatizando deployment con GitHub Actions 🚀",
            "PostgreSQL vs MongoDB: ¿Cuándo usar cada uno? 🗄️",
            "Responsive design: mobile-first siempre 📱",
            "¿Alguien más ama los hooks de React? Código más limpio 🪝",
            "Implementando OAuth2 con Django. Seguridad social media style 🔐",
            "Sass hace que escribir CSS sea un placer 💅",
            "¿Vuestro IDE favorito para Python? VS Code team aquí! 💻",
            "Deployment con Docker Compose: desarrollo y producción identical 🐋",
            "¿Algún consejo para manejar estados complejos en React? 🎭",
            "Django admin es una maravilla para prototipos rápidos ⚡",
            "¿Alguien usa Celery para tareas asíncronas? 🔄",
            "Webpack vs Vite: la velocidad de desarrollo importa 📦",
            "¿Mejores librerías para testing en JavaScript? Jest team 🃏",
            "Trabajando con APIs externas: siempre manejar errores 🛡️",
            "¿Consejos para optimizar SEO en SPAs? 🔍",
            "Django migrations: versionado de base de datos automático 📈",
            "¿Alguien más piensa que Python es perfecto para principiantes? 🐍",
            "Implementando PWA features. Offline-first approach 📱",
        ]

        created_posts = []
        for i in range(num_posts):
            post_content = random.choice(posts_content)
            post_date = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            post = Post.objects.create(
                post_content=post_content,
                post_date=post_date,
                username=random.choice(created_users)
            )
            
            # Agregar likes aleatorios
            num_likes = random.randint(0, len(created_users) // 2)
            random_users_for_likes = random.sample(created_users, num_likes)
            for user in random_users_for_likes:
                post.likes.add(user)
            
            # Agregar tags aleatorios
            num_tags = random.randint(1, 3)
            random_types = random.sample(created_types, num_tags)
            for type_obj in random_types:
                PostTag.objects.create(post_id=post, type_id=type_obj)
            
            created_posts.append(post)
            
        self.stdout.write(f'Creados {len(created_posts)} posts')

        # Crear comentarios
        self.stdout.write('Creando comentarios...')
        comments_content = [
            "¡Excelente post! Me ha sido muy útil 👍",
            "Gracias por compartir, muy interesante",
            "¿Podrías elaborar más sobre este punto?",
            "Totalmente de acuerdo contigo",
            "He tenido la misma experiencia",
            "¡Gran consejo! Lo pondré en práctica",
            "¿Has probado también esta alternativa?",
            "Me encanta este enfoque",
            "Muy bien explicado, gracias",
            "¿Tienes algún recurso adicional sobre esto?",
            "Interesante perspectiva",
            "Esto me ayudó mucho, gracias",
            "¿Cómo manejas los errores en este caso?",
            "Genial, justo lo que necesitaba",
            "¿Performance issues con este approach?",
            "Love it! 💙",
            "¿Algún tutorial que recomiendes?",
            "Saved for later reference 📌",
            "¡Brilliant solution!",
            "This is exactly what I was looking for",
        ]

        for i in range(num_comments):
            comment_content = random.choice(comments_content)
            comment_date = timezone.now() - timedelta(
                days=random.randint(0, 25),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            Comment.objects.create(
                comment_content=comment_content,
                comment_date=comment_date,
                username=random.choice(created_users),
                post_id=random.choice(created_posts)
            )
            
        self.stdout.write(f'Creados {num_comments} comentarios')

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Datos dummy creados exitosamente!\n'
                f'   - {len(created_users)} usuarios\n'
                f'   - {len(created_types)} tipos/categorías\n'
                f'   - {len(created_posts)} posts\n'
                f'   - {num_comments} comentarios'
            )
        )