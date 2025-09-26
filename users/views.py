from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import UserRegisterForm, UserUpdateForm


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


@login_required
def account_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil se actualizó correctamente.')
            return redirect('account-edit')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/account_form.html', {'form': form})


@login_required
def account_delete(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Tu cuenta se eliminó correctamente.')
        return redirect('blog-home')
    return render(request, 'users/account_confirm_delete.html')
