"""
Servicios para interactuar con Neo4j
Proporciona funciones de alto nivel para operaciones de la red social
"""
from datetime import datetime
from typing import List, Dict, Optional
from neomodel import db
from .neo4j_models import UserNode, PostNode, CommentNode, InterestNode
from . import neo4j_connection  # Importar para inicializar conexión
import re


class Neo4jUserService:
    """Servicios relacionados con usuarios"""
    
    @staticmethod
    def create_or_update_user(user_id: int, username: str, email: str, 
                             first_name: str = '', last_name: str = '', bio: str = ''):
        """
        Crea o actualiza un usuario en Neo4j
        """
        try:
            user = UserNode.nodes.get_or_none(user_id=user_id)
            if user:
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.bio = bio
                user.save()
            else:
                user = UserNode(
                    user_id=user_id,
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio
                ).save()
            return user
        except Exception as e:
            print(f"Error creando/actualizando usuario: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Obtiene un usuario por su ID"""
        return UserNode.nodes.get_or_none(user_id=user_id)
    
    @staticmethod
    def get_user_by_username(username: str):
        """Obtiene un usuario por su username"""
        return UserNode.nodes.get_or_none(username=username)
    
    @staticmethod
    def delete_user(user_id: int):
        """Elimina un usuario y todas sus relaciones"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        if user:
            user.delete()
            return True
        return False
    
    @staticmethod
    def follow_user(follower_id: int, followed_id: int):
        """Un usuario sigue a otro"""
        follower = UserNode.nodes.get_or_none(user_id=follower_id)
        followed = UserNode.nodes.get_or_none(user_id=followed_id)
        
        if follower and followed:
            follower.following.connect(followed)
            return True
        return False
    
    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int):
        """Un usuario deja de seguir a otro"""
        follower = UserNode.nodes.get_or_none(user_id=follower_id)
        followed = UserNode.nodes.get_or_none(user_id=followed_id)
        
        if follower and followed:
            follower.following.disconnect(followed)
            return True
        return False
    
    @staticmethod
    def add_friend(user1_id: int, user2_id: int):
        """Agrega una relación de amistad bidireccional"""
        user1 = UserNode.nodes.get_or_none(user_id=user1_id)
        user2 = UserNode.nodes.get_or_none(user_id=user2_id)
        
        if user1 and user2:
            user1.friends.connect(user2)
            user2.friends.connect(user1)
            return True
        return False
    
    @staticmethod
    def remove_friend(user1_id: int, user2_id: int):
        """Elimina una relación de amistad"""
        user1 = UserNode.nodes.get_or_none(user_id=user1_id)
        user2 = UserNode.nodes.get_or_none(user_id=user2_id)
        
        if user1 and user2:
            user1.friends.disconnect(user2)
            user2.friends.disconnect(user1)
            return True
        return False
    
    @staticmethod
    def get_followers(user_id: int):
        """Obtiene la lista de seguidores de un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        if user:
            return user.followers.all()
        return []
    
    @staticmethod
    def get_following(user_id: int):
        """Obtiene la lista de usuarios que sigue un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        if user:
            return user.following.all()
        return []
    
    @staticmethod
    def get_friends(user_id: int):
        """Obtiene la lista de amigos de un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        if user:
            return user.friends.all()
        return []


class Neo4jPostService:
    """Servicios relacionados con publicaciones"""
    
    @staticmethod
    def create_post(post_id: int, user_id: int, content: str):
        """
        Crea una publicación y la conecta con su autor
        También extrae y asocia hashtags
        """
        try:
            user = UserNode.nodes.get_or_none(user_id=user_id)
            if not user:
                return None
            
            post = PostNode(
                post_id=post_id,
                content=content
            ).save()
            
            # Conectar el post con su autor
            user.posts.connect(post)
            
            # Extraer y asociar hashtags
            hashtags = re.findall(r"#(\w+)", content)
            for tag_name in hashtags:
                tag_name = tag_name.lower()
                interest = InterestNode.nodes.get_or_none(name=tag_name)
                if not interest:
                    interest = InterestNode(name=tag_name).save()
                post.tags.connect(interest)
            
            return post
        except Exception as e:
            print(f"Error creando post: {e}")
            return None
    
    @staticmethod
    def update_post(post_id: int, content: str):
        """Actualiza el contenido de una publicación"""
        post = PostNode.nodes.get_or_none(post_id=post_id)
        if post:
            post.content = content
            post.updated_at = datetime.now()
            post.save()
            
            # Actualizar hashtags
            # Primero eliminar los existentes
            for tag in post.tags.all():
                post.tags.disconnect(tag)
            
            # Luego agregar los nuevos
            hashtags = re.findall(r"#(\w+)", content)
            for tag_name in hashtags:
                tag_name = tag_name.lower()
                interest = InterestNode.nodes.get_or_none(name=tag_name)
                if not interest:
                    interest = InterestNode(name=tag_name).save()
                post.tags.connect(interest)
            
            return post
        return None
    
    @staticmethod
    def delete_post(post_id: int):
        """Elimina una publicación"""
        post = PostNode.nodes.get_or_none(post_id=post_id)
        if post:
            post.delete()
            return True
        return False
    
    @staticmethod
    def get_post_by_id(post_id: int):
        """Obtiene una publicación por su ID"""
        return PostNode.nodes.get_or_none(post_id=post_id)
    
    @staticmethod
    def get_user_posts(user_id: int, limit: int = 20):
        """Obtiene todas las publicaciones de un usuario"""
        query = """
        MATCH (u:UserNode {user_id: $user_id})-[:POSTED]->(p:PostNode)
        RETURN p
        ORDER BY p.created_at DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'user_id': user_id, 'limit': limit})
        return [PostNode.inflate(row[0]) for row in results]
    
    @staticmethod
    def get_all_posts(limit: int = 50):
        """Obtiene todas las publicaciones ordenadas por fecha"""
        query = """
        MATCH (p:PostNode)
        RETURN p
        ORDER BY p.created_at DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'limit': limit})
        return [PostNode.inflate(row[0]) for row in results]
    
    @staticmethod
    def get_feed_posts(user_id: int, limit: int = 50):
        """
        Obtiene el feed de un usuario (posts de quien sigue + propios)
        """
        query = """
        MATCH (u:UserNode {user_id: $user_id})
        OPTIONAL MATCH (u)-[:FOLLOWS]->(followed:UserNode)-[:POSTED]->(p:PostNode)
        OPTIONAL MATCH (u)-[:POSTED]->(own_post:PostNode)
        WITH collect(DISTINCT p) + collect(DISTINCT own_post) as all_posts
        UNWIND all_posts as post
        WHERE post IS NOT NULL
        RETURN post
        ORDER BY post.created_at DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'user_id': user_id, 'limit': limit})
        return [PostNode.inflate(row[0]) for row in results]
    
    @staticmethod
    def like_post(user_id: int, post_id: int):
        """Un usuario da like a una publicación"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        post = PostNode.nodes.get_or_none(post_id=post_id)
        
        if user and post:
            user.liked_posts.connect(post)
            return True
        return False
    
    @staticmethod
    def unlike_post(user_id: int, post_id: int):
        """Un usuario quita el like de una publicación"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        post = PostNode.nodes.get_or_none(post_id=post_id)
        
        if user and post:
            user.liked_posts.disconnect(post)
            return True
        return False
    
    @staticmethod
    def get_post_likes_count(post_id: int):
        """Obtiene el número de likes de una publicación"""
        query = """
        MATCH (u:UserNode)-[:LIKES]->(p:PostNode {post_id: $post_id})
        RETURN count(u) as likes_count
        """
        results, meta = db.cypher_query(query, {'post_id': post_id})
        return results[0][0] if results else 0
    
    @staticmethod
    def user_has_liked_post(user_id: int, post_id: int):
        """Verifica si un usuario ha dado like a una publicación"""
        query = """
        MATCH (u:UserNode {user_id: $user_id})-[:LIKES]->(p:PostNode {post_id: $post_id})
        RETURN count(*) > 0 as has_liked
        """
        results, meta = db.cypher_query(query, {'user_id': user_id, 'post_id': post_id})
        return results[0][0] if results else False


class Neo4jCommentService:
    """Servicios relacionados con comentarios"""
    
    @staticmethod
    def create_comment(comment_id: int, user_id: int, post_id: int, content: str):
        """Crea un comentario en una publicación"""
        try:
            user = UserNode.nodes.get_or_none(user_id=user_id)
            post = PostNode.nodes.get_or_none(post_id=post_id)
            
            if not user or not post:
                return None
            
            comment = CommentNode(
                comment_id=comment_id,
                content=content
            ).save()
            
            # Conectar el comentario con su autor y el post
            user.comments.connect(comment)
            comment.post.connect(post)
            
            return comment
        except Exception as e:
            print(f"Error creando comentario: {e}")
            return None
    
    @staticmethod
    def delete_comment(comment_id: int):
        """Elimina un comentario"""
        comment = CommentNode.nodes.get_or_none(comment_id=comment_id)
        if comment:
            comment.delete()
            return True
        return False
    
    @staticmethod
    def get_post_comments(post_id: int):
        """Obtiene todos los comentarios de una publicación"""
        query = """
        MATCH (c:CommentNode)-[:COMMENT_ON]->(p:PostNode {post_id: $post_id})
        RETURN c
        ORDER BY c.created_at DESC
        """
        results, meta = db.cypher_query(query, {'post_id': post_id})
        return [CommentNode.inflate(row[0]) for row in results]


class Neo4jInterestService:
    """Servicios relacionados con intereses"""
    
    @staticmethod
    def add_user_interest(user_id: int, interest_name: str):
        """Agrega un interés a un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        interest = InterestNode.nodes.get_or_none(name=interest_name.lower())
        
        if not interest:
            interest = InterestNode(name=interest_name.lower()).save()
        
        if user and interest:
            user.interests.connect(interest)
            return True
        return False
    
    @staticmethod
    def remove_user_interest(user_id: int, interest_name: str):
        """Elimina un interés de un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        interest = InterestNode.nodes.get_or_none(name=interest_name.lower())
        
        if user and interest:
            user.interests.disconnect(interest)
            return True
        return False
    
    @staticmethod
    def get_user_interests(user_id: int):
        """Obtiene todos los intereses de un usuario"""
        user = UserNode.nodes.get_or_none(user_id=user_id)
        if user:
            return user.interests.all()
        return []
    
    @staticmethod
    def get_posts_by_interest(interest_name: str, limit: int = 50):
        """Obtiene publicaciones etiquetadas con un interés específico"""
        query = """
        MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode {name: $interest_name})
        RETURN p
        ORDER BY p.created_at DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'interest_name': interest_name.lower(), 'limit': limit})
        return [PostNode.inflate(row[0]) for row in results]


class Neo4jAnalyticsService:
    """Servicios de análisis y recomendaciones basados en grafos"""
    
    @staticmethod
    def suggest_friends(user_id: int, limit: int = 10):
        """
        Sugiere amigos basándose en amigos en común
        (Amigos de amigos que no son amigos del usuario)
        """
        query = """
        MATCH (u:UserNode {user_id: $user_id})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(suggestion)
        WHERE NOT (u)-[:FRIEND_OF]->(suggestion) AND u <> suggestion
        WITH suggestion, count(*) as common_friends
        RETURN suggestion, common_friends
        ORDER BY common_friends DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'user_id': user_id, 'limit': limit})
        return [
            {
                'user': UserNode.inflate(row[0]),
                'common_friends': row[1]
            }
            for row in results
        ]
    
    @staticmethod
    def suggest_users_to_follow(user_id: int, limit: int = 10):
        """
        Sugiere usuarios para seguir basándose en intereses comunes
        """
        query = """
        MATCH (u:UserNode {user_id: $user_id})-[:INTERESTED_IN]->(i:InterestNode)<-[:INTERESTED_IN]-(suggestion)
        WHERE NOT (u)-[:FOLLOWS]->(suggestion) AND u <> suggestion
        WITH suggestion, count(DISTINCT i) as common_interests
        RETURN suggestion, common_interests
        ORDER BY common_interests DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'user_id': user_id, 'limit': limit})
        return [
            {
                'user': UserNode.inflate(row[0]),
                'common_interests': row[1]
            }
            for row in results
        ]
    
    @staticmethod
    def get_common_interests(user1_id: int, user2_id: int):
        """Obtiene los intereses comunes entre dos usuarios"""
        query = """
        MATCH (u1:UserNode {user_id: $user1_id})-[:INTERESTED_IN]->(i:InterestNode)<-[:INTERESTED_IN]-(u2:UserNode {user_id: $user2_id})
        RETURN i
        """
        results, meta = db.cypher_query(query, {'user1_id': user1_id, 'user2_id': user2_id})
        return [InterestNode.inflate(row[0]) for row in results]
    
    @staticmethod
    def get_trending_interests(limit: int = 10):
        """Obtiene los intereses más populares (con más posts)"""
        query = """
        MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode)
        WITH i, count(p) as post_count
        RETURN i, post_count
        ORDER BY post_count DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'limit': limit})
        return [
            {
                'interest': InterestNode.inflate(row[0]),
                'count': row[1]
            }
            for row in results
        ]
    
    @staticmethod
    def get_influencers(limit: int = 10):
        """Obtiene los usuarios más influyentes (con más seguidores)"""
        query = """
        MATCH (u:UserNode)<-[:FOLLOWS]-(follower)
        WITH u, count(follower) as follower_count
        RETURN u, follower_count
        ORDER BY follower_count DESC
        LIMIT $limit
        """
        results, meta = db.cypher_query(query, {'limit': limit})
        return [
            {
                'user': UserNode.inflate(row[0]),
                'followers': row[1]
            }
            for row in results
        ]
    
    @staticmethod
    def get_user_network_stats(user_id: int):
        """Obtiene estadísticas de la red de un usuario"""
        query = """
        MATCH (u:UserNode {user_id: $user_id})
        OPTIONAL MATCH (u)-[:FOLLOWS]->(following)
        OPTIONAL MATCH (u)<-[:FOLLOWS]-(follower)
        OPTIONAL MATCH (u)-[:FRIEND_OF]-(friend)
        OPTIONAL MATCH (u)-[:POSTED]->(post)
        OPTIONAL MATCH (u)-[:INTERESTED_IN]->(interest)
        RETURN 
            count(DISTINCT following) as following_count,
            count(DISTINCT follower) as followers_count,
            count(DISTINCT friend) as friends_count,
            count(DISTINCT post) as posts_count,
            count(DISTINCT interest) as interests_count
        """
        results, meta = db.cypher_query(query, {'user_id': user_id})
        if results:
            return {
                'following': results[0][0],
                'followers': results[0][1],
                'friends': results[0][2],
                'posts': results[0][3],
                'interests': results[0][4]
            }
        return None
