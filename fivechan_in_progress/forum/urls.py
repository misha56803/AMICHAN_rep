from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
]

urlpatterns += [
    path('accounts/register/', views.register, name='register'),
]