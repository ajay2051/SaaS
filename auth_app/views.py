from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


def login_view(request):
    """
    Login View for All Users
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/visits')
        context = {}
    return render(request, 'login.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        if user:
            raise ValueError("User already exists")
        user.save()
        return redirect('/auth_app/login')
    return render(request, 'register.html', context={})


VALID_CODE = 'abc123'


@login_required
def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == 'POST':
        password_sent = request.POST.get('code') or None
        if password_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = 1
    if is_allowed:
        return redirect('home_page')
    return render(request, 'pw_protected.html', context={})


@login_required
@staff_member_required
def user_only_page_view(request, *args, **kwargs):
    return render(request, 'user_only_page.html', context={})


@login_required
def profile_view(request, username=None, *args, **kwargs):
    profile_user_obj = get_object_or_404(User, username=username)
    return HttpResponse(f'Hello, {username} - {profile_user_obj.id}. You\'re at the profile page.')


@login_required
def profile_list_view(request, *args, **kwargs):
    users = User.objects.filter(is_active=True)
    context = {'users': users}
    return render(request, 'profile_list.html', context)
