from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from blog.neo4j_services import Neo4jUserService

@receiver(post_save, sender=User)
def sync_user_to_neo4j(sender, instance, created, **kwargs):
    """
    Signal que sincroniza automáticamente usuarios de Django a Neo4j
    Se ejecuta cada vez que se crea o actualiza un usuario
    """
    try:
        # Sincronizar usuario a Neo4j
        Neo4jUserService.create_or_update_user(
            user_id=instance.id,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            bio=getattr(instance.profile, 'bio', '') if hasattr(instance, 'profile') else ''
        )
        
        if created:
            print(f"✅ Usuario '{instance.username}' creado y sincronizado con Neo4j")
        else:
            print(f"✅ Usuario '{instance.username}' actualizado en Neo4j")
            
    except Exception as e:
        print(f"⚠️ Error sincronizando usuario {instance.username} a Neo4j: {str(e)}")

