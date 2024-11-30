from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
]

# Аутентификация
urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', auth_views.LoginView.as_view(template_name='registration/register.html'), name='register'),
]