from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    context = {}
    return render(request, 'auth_app/login.html', context=context)
