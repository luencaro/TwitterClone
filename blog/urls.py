from django.urls import path
from django.shortcuts import redirect
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentUpdateView,
    CommentDeleteView,
    post_list)
from . import views
from . import social_views
from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/',views.about, name='blog-about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    # Redirigir user-posts a user-profile-network para unificar vistas
    path('user/<str:username>', lambda request, username: redirect('user-profile-network', username=username), name='user-posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('l/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/posts', post_list),
    
    # Rutas de red social con Neo4j
    path('friends/', social_views.friends_list, name='friends-list'),
    path('friends/add/<int:user_id>/', social_views.add_friend, name='add-friend'),
    path('friends/remove/<int:user_id>/', social_views.remove_friend, name='remove-friend'),
    path('follow/<int:user_id>/', social_views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', social_views.unfollow_user, name='unfollow-user'),
    path('followers/', social_views.followers_list, name='followers-list'),
    path('followers/<str:username>/', social_views.followers_list, name='followers-list'),
    path('following/', social_views.following_list, name='following-list'),
    path('following/<str:username>/', social_views.following_list, name='following-list'),
    path('interests/', social_views.interests_list, name='interests-list'),
    path('interests/<str:interest_name>/', social_views.posts_by_interest, name='posts-by-interest'),
    path('analytics/', social_views.network_analytics, name='network-analytics'),
    path('profile/<str:username>/', social_views.user_profile_network, name='user-profile-network'),
    
    # APIs para widgets sociales
    path('api/friend-suggestions/', social_views.api_friend_suggestions, name='api-friend-suggestions'),
    path('api/trending-topics/', social_views.api_trending_topics, name='api-trending-topics'),
    path('api/influencers/', social_views.api_influencers, name='api-influencers'),
    path('api/follow/<int:user_id>/', social_views.api_follow_user, name='api-follow-user'),
    path('api/unfollow/<int:user_id>/', social_views.api_unfollow_user, name='api-unfollow-user'),
]
