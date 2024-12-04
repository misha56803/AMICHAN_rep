from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from forum import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout') 
]

urlpatterns += [
    path('accounts/register/', views.register, name='register'),
    path('accounts/confirm/<str:uid>/<str:token>/', views.confirm_email, name='confirm_email'),
]