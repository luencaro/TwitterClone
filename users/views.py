from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('search', '').strip()
        results = User.objects.filter(username__icontains=query)
        return render(request, 'users/search_result.html', {'results': results, 'query': query})
    return redirect('blog-home')
