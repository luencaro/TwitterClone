from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view

from .forms import NewCommentForm
from .models import Comment, Post, Type
from .serializers import GroupSerializer, PostSerializer, UserSerializer

PAGINATION_COUNT = 10


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
                Prefetch('comments', queryset=Comment.objects.select_related('username'))
            )
        )
        type_name = self.request.GET.get('type')
        if type_name:
            queryset = queryset.filter(post_tags__type_id__type_name=type_name)
        return queryset.order_by('-post_date').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all().order_by('type_name')
        context['active_type'] = self.request.GET.get('type')
        context['comment_form'] = NewCommentForm()
        return context


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
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_content']
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['post_content']
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

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

    def test_func(self):
        post = self.get_object()
        return post.username == self.request.user


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
