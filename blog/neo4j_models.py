"""
Modelos de Neo4j usando neomodel
Define los nodos y relaciones para la red social
"""
from datetime import datetime
from neomodel import (
    StructuredNode, StringProperty, IntegerProperty, 
    DateTimeProperty, RelationshipTo, RelationshipFrom,
    Relationship, UniqueIdProperty, BooleanProperty
)


class UserNode(StructuredNode):
    """
    Nodo que representa un usuario en la red social
    """
    # Propiedades del usuario
    user_id = IntegerProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True, required=True)
    email = StringProperty(required=True)
    first_name = StringProperty(default='')
    last_name = StringProperty(default='')
    bio = StringProperty(default='')
    date_joined = DateTimeProperty(default_now=True)
    
    # Relaciones
    posts = RelationshipTo('PostNode', 'POSTED')
    comments = RelationshipTo('CommentNode', 'COMMENTED')
    liked_posts = RelationshipTo('PostNode', 'LIKES')
    following = RelationshipTo('UserNode', 'FOLLOWS')
    followers = RelationshipFrom('UserNode', 'FOLLOWS')
    friends = RelationshipTo('UserNode', 'FRIEND_OF')
    interests = RelationshipTo('InterestNode', 'INTERESTED_IN')
    
    class Meta:
        app_label = 'blog'


class PostNode(StructuredNode):
    """
    Nodo que representa una publicación
    """
    # Propiedades del post
    post_id = IntegerProperty(unique_index=True, required=True)
    content = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    
    # Relaciones
    author = RelationshipFrom('UserNode', 'POSTED')
    comments = RelationshipFrom('CommentNode', 'COMMENT_ON')
    likes = RelationshipFrom('UserNode', 'LIKES')
    tags = RelationshipTo('InterestNode', 'TAGGED_WITH')
    
    class Meta:
        app_label = 'blog'


class CommentNode(StructuredNode):
    """
    Nodo que representa un comentario
    """
    # Propiedades del comentario
    comment_id = IntegerProperty(unique_index=True, required=True)
    content = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    
    # Relaciones
    author = RelationshipFrom('UserNode', 'COMMENTED')
    post = RelationshipTo('PostNode', 'COMMENT_ON')
    
    class Meta:
        app_label = 'blog'


class InterestNode(StructuredNode):
    """
    Nodo que representa un interés/hashtag/categoría
    """
    # Propiedades del interés
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default='')
    created_at = DateTimeProperty(default_now=True)
    
    # Relaciones
    interested_users = RelationshipFrom('UserNode', 'INTERESTED_IN')
    tagged_posts = RelationshipFrom('PostNode', 'TAGGED_WITH')
    
    class Meta:
        app_label = 'blog'


# Relaciones personalizadas con propiedades adicionales

class FollowsRel(Relationship):
    """
    Relación FOLLOWS con fecha de inicio
    """
    since = DateTimeProperty(default_now=True)


class FriendOfRel(Relationship):
    """
    Relación FRIEND_OF con fecha de amistad
    """
    since = DateTimeProperty(default_now=True)
    status = StringProperty(default='pending')  # pending, accepted, rejected


class LikesRel(Relationship):
    """
    Relación LIKES con fecha del like
    """
    liked_at = DateTimeProperty(default_now=True)
