from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.decorators.http import require_POST
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
import re
from urllib.parse import urlencode

from .forms import NewCommentForm, PostForm
from .models import Comment, Post, Type, PostTag
from .serializers import GroupSerializer, PostSerializer, UserSerializer
from .neo4j_services import Neo4jPostService, Neo4jInterestService, Neo4jUserService

PAGINATION_COUNT = 10


def _process_hashtags(post):
    """
    Extrae hashtags del contenido del post, los crea si no existen
    y los asocia con el post.
    """
    # Primero, eliminamos las etiquetas antiguas para evitar duplicados en la edición
    post.post_tags.all().delete()
    
    # Buscamos todas las palabras que comiencen con #
    hashtags = re.findall(r"#(\w+)", post.post_content)
    for tag_name in hashtags:
        # Creamos o obtenemos el 'Type' (hashtag)
        tag, _ = Type.objects.get_or_create(type_name=tag_name.lower())
        # Creamos la relación entre el post y el tag
        PostTag.objects.get_or_create(post_id=post, type_id=tag)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def get_queryset(self):
        queryset = (
            Post.objects
            .select_related('username')
            .prefetch_related(
                Prefetch('comments', queryset=Comment.objects.select_related('username')),
                'post_tags__type_id'
            )
        )
        
        raw_type = (self.request.GET.get('type') or '').strip()
        raw_query_input = (self.request.GET.get('q') or '').strip()
        raw_query = raw_query_input.lstrip('#') if raw_query_input else ''

        self.active_type = None
        self.search_query = raw_query_input or raw_query
        self.requested_type = raw_type
        self.search_value = raw_query_input or raw_query

        def _filter_by_type(name):
            type_obj = Type.objects.filter(type_name__iexact=name).first()
            if not type_obj:
                return queryset.none()
            self.active_type = type_obj.type_name
            return queryset.filter(post_tags__type_id=type_obj)

        if raw_type:
            queryset = _filter_by_type(raw_type)
            if self.active_type:
                self.search_value = f"#{self.active_type}"
        elif raw_query:
            # Si la búsqueda coincide con un hashtag, filtramos por hashtag
            type_obj = Type.objects.filter(type_name__iexact=raw_query).first()
            if type_obj:
                self.active_type = type_obj.type_name
                queryset = queryset.filter(post_tags__type_id=type_obj)
                self.search_value = f"#{self.active_type}"
            else:
                # Búsqueda general
                queryset = queryset.filter(
                    models.Q(post_content__icontains=raw_query) |
                    models.Q(username__username__icontains=raw_query) |
                    models.Q(post_tags__type_id__type_name__icontains=raw_query)
                )
        
        self.current_querystring = ''
        params = {}
        if self.requested_type:
            params['type'] = self.requested_type
        elif self.active_type:
            params['type'] = self.active_type
        elif self.search_query:
            params['q'] = self.search_query
        if params:
            self.current_querystring = urlencode(params)

        return queryset.order_by('-post_date').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = getattr(self, 'search_value', '')
        context['active_type'] = getattr(self, 'active_type', '')
        context['current_querystring'] = getattr(self, 'current_querystring', '')
        context['comment_form'] = NewCommentForm()
        
        # Obtener lista de usuarios que el usuario actual está siguiendo
        try:
            user_service = Neo4jUserService()
            following_users = user_service.get_following(self.request.user.id)
            # Crear un set de user_ids para búsqueda rápida
            context['following_user_ids'] = {user.user_id for user in following_users}
        except Exception as e:
            print(f"Error obteniendo usuarios seguidos: {e}")
            context['following_user_ids'] = set()
        
        return context


@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes': post.number_of_likes})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('blog-home')))


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(username=self.profile_user).order_by('-post_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('username')
        context['form'] = kwargs.get('form', NewCommentForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user
            comment.post_id = self.object
            comment.save()
            
            # Sincronizar con Neo4j
            try:
                from .neo4j_services import Neo4jCommentService
                neo4j_comment_service = Neo4jCommentService()
                neo4j_comment_service.create_comment(
                    comment_id=comment.id,
                    user_id=request.user.id,
                    post_id=self.object.id,
                    content=comment.comment_content
                )
            except Exception as e:
                print(f"Error sincronizando comentario con Neo4j: {e}")
            
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.username = self.request.user
        # Guardamos el objeto para obtener un ID antes de procesar los hashtags
        self.object = form.save()
        _process_hashtags(self.object)
        
        # Sincronizar con Neo4j
        try:
            print(f"🔄 Iniciando sincronización con Neo4j para post {self.object.post_id}")
            neo4j_post_service = Neo4jPostService()
            neo4j_user_service = Neo4jUserService()
            
            # Asegurar que el usuario existe en Neo4j
            user = self.request.user
            neo4j_user_service.create_or_update_user(
                user.id, user.username, user.email,
                user.first_name, user.last_name, user.profile.bio if hasattr(user, 'profile') else ''
            )
            print(f"✅ Usuario {user.username} verificado en Neo4j")
            
            # Crear el post en Neo4j
            neo4j_post_service.create_post(
                post_id=self.object.post_id,
                user_id=user.id,
                content=self.object.post_content
            )
            print(f"✅ Post {self.object.post_id} sincronizado con Neo4j: {self.object.post_content[:50]}...")
            
        except Exception as e:
            print(f"❌ Error sincronizando post {self.object.post_id} con Neo4j: {e}")
            import traceback
            traceback.print_exc()
            # No fallamos la creación del post si Neo4j falla
        
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        # El objeto se guarda automáticamente en UpdateView
        self.object = form.save()
        _process_hashtags(self.object)
        
        # Sincronizar con Neo4j
        try:
            print(f"🔄 Actualizando post {self.object.post_id} en Neo4j")
            neo4j_post_service = Neo4jPostService()
            
            # Actualizar el post en Neo4j
            neo4j_post_service.update_post(
                post_id=self.object.post_id,
                content=self.object.post_content
            )
            print(f"✅ Post {self.object.post_id} actualizado en Neo4j")
            
        except Exception as e:
            print(f"❌ Error sincronizando actualización con Neo4j: {e}")
            import traceback
            traceback.print_exc()
        
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        post = self.get_object()
        return post.username == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog-home')
    
    def delete(self, request, *args, **kwargs):
        # Obtener el objeto antes de eliminarlo
        self.object = self.get_object()
        post_id = self.object.id
        
        # Eliminar de Neo4j primero
        try:
            neo4j_post_service = Neo4jPostService()
            neo4j_post_service.delete_post(post_id)
        except Exception as e:
            print(f"Error eliminando post de Neo4j: {e}")
        
        # Llamar al método delete de la clase padre para eliminar de Django
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return post.username == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = NewCommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post_id.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.username == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        # Obtener el objeto antes de eliminarlo
        self.object = self.get_object()
        comment_id = self.object.id
        
        # Eliminar de Neo4j primero
        try:
            from .neo4j_services import Neo4jCommentService
            neo4j_comment_service = Neo4jCommentService()
            neo4j_comment_service.delete_comment(comment_id)
        except Exception as e:
            print(f"Error eliminando comentario de Neo4j: {e}")
        
        # Llamar al método delete de la clase padre
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post_id.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.username == self.request.user


def about(request):
    return render(request, 'blog/about.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST', 'DELETE'])
def post_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        posts = Post.objects.select_related('username').all().order_by('-post_date')
        post_serializer = PostSerializer(posts, many=True)
        return JsonResponse(post_serializer.data, safe=False)

    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data, context={'request': request})
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    deleted, _ = Post.objects.all().delete()
    return JsonResponse({'message': f'{deleted} posts eliminados correctamente.'}, status=status.HTTP_204_NO_CONTENT)
