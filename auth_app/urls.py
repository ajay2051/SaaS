from django.urls import path

from auth_app import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
]