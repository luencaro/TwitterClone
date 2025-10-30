"""
Vistas para funcionalidades de red social con Neo4j
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .neo4j_services import (
    Neo4jUserService, Neo4jPostService, Neo4jInterestService, 
    Neo4jAnalyticsService
)


@login_required
def friends_list(request):
    """Vista para mostrar la lista de amigos"""
    user_service = Neo4jUserService()
    friends = user_service.get_friends(request.user.id)
    
    # Convertir nodos de Neo4j a usuarios de Django para mostrar en la plantilla
    friends_data = []
    for friend_node in friends:
        try:
            django_user = User.objects.get(id=friend_node.user_id)
            friends_data.append({
                'user': django_user,
                'neo4j_node': friend_node
            })
        except User.DoesNotExist:
            continue
    
    context = {
        'friends': friends_data,
        'title': 'Mis Amigos'
    }
    return render(request, 'blog/friends_list.html', context)


@login_required
def add_friend(request, user_id):
    """Agregar un amigo"""
    if request.method == 'POST':
        user_service = Neo4jUserService()
        success = user_service.add_friend(request.user.id, user_id)
        
        if success:
            messages.success(request, 'Amigo agregado exitosamente')
        else:
            messages.error(request, 'No se pudo agregar el amigo')
    
    return redirect(request.META.get('HTTP_REFERER', 'blog-home'))


@login_required
def remove_friend(request, user_id):
    """Eliminar un amigo"""
    if request.method == 'POST':
        user_service = Neo4jUserService()
        success = user_service.remove_friend(request.user.id, user_id)
        
        if success:
            messages.success(request, 'Amigo eliminado')
        else:
            messages.error(request, 'No se pudo eliminar el amigo')
    
    return redirect(request.META.get('HTTP_REFERER', 'blog-home'))


@login_required
def follow_user(request, user_id):
    """Seguir a un usuario"""
    if request.method == 'POST':
        user_service = Neo4jUserService()
        success = user_service.follow_user(request.user.id, user_id)
        
        if success:
            messages.success(request, 'Ahora sigues a este usuario')
        else:
            messages.error(request, 'No se pudo seguir al usuario')
    
    return redirect(request.META.get('HTTP_REFERER', 'blog-home'))


@login_required
def unfollow_user(request, user_id):
    """Dejar de seguir a un usuario"""
    if request.method == 'POST':
        user_service = Neo4jUserService()
        success = user_service.unfollow_user(request.user.id, user_id)
        
        if success:
            messages.success(request, 'Dejaste de seguir a este usuario')
        else:
            messages.error(request, 'No se pudo dejar de seguir al usuario')
    
    return redirect(request.META.get('HTTP_REFERER', 'blog-home'))


@login_required
def followers_list(request, username=None):
    """Vista para mostrar seguidores de un usuario"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    user_service = Neo4jUserService()
    followers = user_service.get_followers(user.id)
    
    followers_data = []
    for follower_node in followers:
        try:
            django_user = User.objects.get(id=follower_node.user_id)
            followers_data.append({
                'user': django_user,
                'neo4j_node': follower_node
            })
        except User.DoesNotExist:
            continue
    
    context = {
        'followers': followers_data,
        'profile_user': user,
        'title': f'Seguidores de {user.username}'
    }
    return render(request, 'blog/followers_list.html', context)


@login_required
def following_list(request, username=None):
    """Vista para mostrar a quién sigue un usuario"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    user_service = Neo4jUserService()
    following = user_service.get_following(user.id)
    
    following_data = []
    for followed_node in following:
        try:
            django_user = User.objects.get(id=followed_node.user_id)
            following_data.append({
                'user': django_user,
                'neo4j_node': followed_node
            })
        except User.DoesNotExist:
            continue
    
    context = {
        'following': following_data,
        'profile_user': user,
        'title': f'{user.username} sigue a'
    }
    return render(request, 'blog/following_list.html', context)


@login_required
def interests_list(request):
    """Vista para mostrar y gestionar intereses del usuario"""
    interest_service = Neo4jInterestService()
    user_interests = interest_service.get_user_interests(request.user.id)
    
    if request.method == 'POST':
        interest_name = request.POST.get('interest_name', '').strip()
        action = request.POST.get('action')
        
        if action == 'add' and interest_name:
            success = interest_service.add_user_interest(request.user.id, interest_name)
            if success:
                messages.success(request, f'Interés "{interest_name}" agregado')
            else:
                messages.error(request, 'No se pudo agregar el interés')
        elif action == 'remove' and interest_name:
            success = interest_service.remove_user_interest(request.user.id, interest_name)
            if success:
                messages.success(request, f'Interés "{interest_name}" eliminado')
            else:
                messages.error(request, 'No se pudo eliminar el interés')
        
        return redirect('interests-list')
    
    # Obtener intereses trending para sugerencias
    trending = Neo4jAnalyticsService.get_trending_interests(limit=15)
    
    context = {
        'user_interests': user_interests,
        'trending_interests': trending,
        'title': 'Mis Intereses'
    }
    return render(request, 'blog/interests_list.html', context)


@login_required
def posts_by_interest(request, interest_name):
    """Vista para mostrar posts de un interés específico"""
    interest_service = Neo4jInterestService()
    posts = interest_service.get_posts_by_interest(interest_name, limit=50)
    
    # Convertir posts de Neo4j a datos con información del autor
    posts_data = []
    for post_node in posts:
        # Obtener autor del post
        author_rel = post_node.author.all()
        if author_rel:
            author_node = author_rel[0]
            try:
                django_user = User.objects.get(id=author_node.user_id)
                posts_data.append({
                    'post': post_node,
                    'author': django_user
                })
            except User.DoesNotExist:
                continue
    
    context = {
        'posts': posts_data,
        'interest_name': interest_name,
        'title': f'Posts sobre #{interest_name}'
    }
    return render(request, 'blog/posts_by_interest.html', context)


@login_required
def network_analytics(request):
    """Vista de análisis de red"""
    analytics = Neo4jAnalyticsService()
    
    # Obtener estadísticas del usuario
    user_stats = analytics.get_user_network_stats(request.user.id)
    
    # Obtener sugerencias (solo usuarios para seguir, no amigos)
    suggested_to_follow = analytics.suggest_users_to_follow(request.user.id, limit=10)
    
    # Convertir a datos para template
    suggested_to_follow_data = []
    for suggestion in suggested_to_follow:
        try:
            user_node = suggestion['user']
            django_user = User.objects.get(id=user_node.user_id)
            suggested_to_follow_data.append({
                'user': django_user,
                'common_interests': suggestion['common_interests'],
                'neo4j_node': user_node
            })
        except User.DoesNotExist:
            continue
    
    # Obtener influencers (ahora devuelve diccionarios)
    influencers = analytics.get_influencers(limit=10)
    influencers_data = []
    for influencer in influencers:
        try:
            user_node = influencer['user']
            django_user = User.objects.get(id=user_node.user_id)
            influencers_data.append({
                'user': django_user,
                'followers': influencer['followers'],
                'neo4j_node': user_node
            })
        except User.DoesNotExist:
            continue
    
    # Intereses trending (ahora devuelve diccionarios)
    trending_interests = analytics.get_trending_interests(limit=10)
    
    context = {
        'user_stats': user_stats,
        'suggested_to_follow': suggested_to_follow_data,
        'influencers': influencers_data,
        'trending_interests': trending_interests,
        'title': 'Análisis de Red'
    }
    return render(request, 'blog/network_analytics.html', context)


@login_required
def user_profile_network(request, username):
    """Vista de perfil de usuario con posts y estadísticas de red"""
    from .models import Post
    from django.core.paginator import Paginator
    
    user = get_object_or_404(User, username=username)
    analytics = Neo4jAnalyticsService()
    user_service = Neo4jUserService()
    
    # Obtener estadísticas del usuario
    user_stats = analytics.get_user_network_stats(user.id)
    
    # Verificar si el usuario actual sigue al perfil
    is_following = False
    
    if request.user.id != user.id:
        # Verificar si sigue
        following = user_service.get_following(request.user.id)
        is_following = any(f.user_id == user.id for f in following)
    
    # Obtener intereses del usuario
    interest_service = Neo4jInterestService()
    user_interests = interest_service.get_user_interests(user.id)
    
    # Obtener posts del usuario
    posts_list = Post.objects.filter(username=user).order_by('-post_date')
    paginator = Paginator(posts_list, 10)  # 10 posts por página
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Obtener lista de usuarios que el usuario actual está siguiendo (para botones de seguir)
    try:
        following_users = user_service.get_following(request.user.id)
        following_user_ids = {u.user_id for u in following_users}
    except Exception as e:
        print(f"Error obteniendo usuarios seguidos: {e}")
        following_user_ids = set()
    
    context = {
        'profile_user': user,
        'user_stats': user_stats,
        'is_following': is_following,
        'user_interests': user_interests,
        'posts': posts,
        'following_user_ids': following_user_ids,
        'title': f'Perfil de {user.username}'
    }
    return render(request, 'blog/user_profile_network.html', context)


# ============================================
# APIs para widgets sociales
# ============================================

@login_required
def api_friend_suggestions(request):
    """API para obtener sugerencias de usuarios para seguir (basado en intereses comunes)"""
    analytics = Neo4jAnalyticsService()
    # Cambiar de suggest_friends a suggest_users_to_follow
    suggestions = analytics.suggest_users_to_follow(request.user.id)
    
    # Convertir a formato JSON
    suggestions_data = []
    for suggestion in suggestions[:5]:  # Top 5 sugerencias
        try:
            django_user = User.objects.get(id=suggestion['user'].user_id)
            suggestions_data.append({
                'user_id': django_user.id,
                'username': django_user.username,
                'common_interests': suggestion['common_interests']  # Cambiado de common_friends
            })
        except User.DoesNotExist:
            continue
    
    return JsonResponse({'suggestions': suggestions_data})



@login_required
def api_trending_topics(request):
    """API para obtener trending topics"""
    analytics = Neo4jAnalyticsService()
    trending = analytics.get_trending_interests()
    
    trending_data = [
        {
            'name': topic['interest'].name,
            'count': topic['count']
        }
        for topic in trending[:10]  # Top 10 trending
    ]
    
    return JsonResponse({'trending': trending_data})


@login_required
def api_influencers(request):
    """API para obtener usuarios influencers"""
    analytics = Neo4jAnalyticsService()
    influencers = analytics.get_influencers()
    
    influencers_data = []
    for influencer in influencers[:5]:  # Top 5 influencers
        try:
            django_user = User.objects.get(id=influencer['user'].user_id)
            influencers_data.append({
                'user_id': django_user.id,
                'username': django_user.username,
                'followers': influencer['followers']
            })
        except User.DoesNotExist:
            continue
    
    return JsonResponse({'influencers': influencers_data})


@login_required
def api_follow_user(request, user_id):
    """API para seguir a un usuario"""
    if request.method == 'POST':
        try:
            # Obtener el usuario a seguir
            user_to_follow = User.objects.get(id=user_id)
            
            print(f"DEBUG: Usuario {request.user.id} ({request.user.username}) intentando seguir a {user_id} ({user_to_follow.username})")
            
            # Crear o actualizar ambos usuarios en Neo4j
            user_service = Neo4jUserService()
            
            # Asegurar que el usuario actual existe en Neo4j
            current_user = request.user
            print(f"DEBUG: Creando/actualizando usuario actual {current_user.id} en Neo4j")
            user_service.create_or_update_user(
                current_user.id, 
                current_user.username, 
                current_user.email,
                current_user.first_name, 
                current_user.last_name, 
                current_user.profile.bio if hasattr(current_user, 'profile') else ''
            )
            
            # Asegurar que el usuario a seguir existe en Neo4j
            print(f"DEBUG: Creando/actualizando usuario a seguir {user_to_follow.id} en Neo4j")
            user_service.create_or_update_user(
                user_to_follow.id,
                user_to_follow.username,
                user_to_follow.email,
                user_to_follow.first_name,
                user_to_follow.last_name,
                user_to_follow.profile.bio if hasattr(user_to_follow, 'profile') else ''
            )
            
            # Ahora sí, crear la relación de seguimiento
            print(f"DEBUG: Creando relación de seguimiento")
            success = user_service.follow_user(request.user.id, user_id)
            print(f"DEBUG: Resultado follow_user: {success}")
            return JsonResponse({'success': success})
        except User.DoesNotExist:
            print(f"ERROR: Usuario {user_id} no encontrado")
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            print(f"ERROR en api_follow_user: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False}, status=400)


@login_required
def api_unfollow_user(request, user_id):
    """API para dejar de seguir a un usuario"""
    if request.method == 'POST':
        try:
            # Verificar que el usuario existe
            user_to_unfollow = User.objects.get(id=user_id)
            
            # Dejar de seguir
            user_service = Neo4jUserService()
            success = user_service.unfollow_user(request.user.id, user_id)
            return JsonResponse({'success': success})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            print(f"Error en api_unfollow_user: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False}, status=400)


@login_required
def network_graph_view(request, username):
    """Vista para visualización gráfica de la red de conexiones de un usuario"""
    user = get_object_or_404(User, username=username)
    
    context = {
        'profile_user': user,
        'title': f'Red de Conexiones - {user.username}'
    }
    return render(request, 'blog/network_graph.html', context)


@login_required
def network_graph_data(request, username):
    """API que devuelve datos de la red en formato JSON para la visualización"""
    user = get_object_or_404(User, username=username)
    user_service = Neo4jUserService()
    
    try:
        # Obtener seguidores y seguidos del usuario
        followers = user_service.get_followers(user.id)
        following = user_service.get_following(user.id)
        
        # Crear conjunto de nodos (usuarios únicos)
        nodes = {}
        edges = []
        
        # Agregar el usuario principal
        nodes[user.id] = {
            'id': user.id,
            'label': user.username,
            'level': 0,  # Usuario central
            'color': '#1da1f2',  # Color azul Twitter para el usuario principal
            'size': 30,
            'font': {'size': 16, 'color': '#ffffff', 'face': 'Arial'}
        }
        
        # Agregar seguidores
        for follower_data in followers:
            follower_user = User.objects.get(id=follower_data.user_id)
            if follower_user.id not in nodes:
                nodes[follower_user.id] = {
                    'id': follower_user.id,
                    'label': follower_user.username,
                    'level': 1,
                    'color': '#17bf63',  # Verde para seguidores
                    'size': 20,
                    'font': {'size': 12}
                }
            # Crear arista: follower -> usuario principal
            edges.append({
                'from': follower_user.id,
                'to': user.id,
                'arrows': 'to',
                'color': {'color': '#17bf63', 'opacity': 0.6}
            })
        
        # Agregar seguidos
        for following_data in following:
            followed_user = User.objects.get(id=following_data.user_id)
            if followed_user.id not in nodes:
                nodes[followed_user.id] = {
                    'id': followed_user.id,
                    'label': followed_user.username,
                    'level': 1,
                    'color': '#e1306c',  # Rosa para seguidos
                    'size': 20,
                    'font': {'size': 12}
                }
            # Crear arista: usuario principal -> seguido
            edges.append({
                'from': user.id,
                'to': followed_user.id,
                'arrows': 'to',
                'color': {'color': '#e1306c', 'opacity': 0.6}
            })
        
        # Convertir nodos a lista
        nodes_list = list(nodes.values())
        
        return JsonResponse({
            'nodes': nodes_list,
            'edges': edges,
            'stats': {
                'followers': len(followers),
                'following': len(following),
                'total_nodes': len(nodes_list)
            }
        })
        
    except Exception as e:
        print(f"Error en network_graph_data: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
