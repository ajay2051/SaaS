from django.urls import path

from auth_app import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('pw_protect/', views.pw_protected_view, name='pw_protect'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
