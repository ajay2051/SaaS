from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_view(request):
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
