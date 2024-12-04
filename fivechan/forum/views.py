from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse


from .utils import send_confirmation_email
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm, CustomUserCreationForm
from . import views

def main_page(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'main_page.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = thread.comments.all().order_by('created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = CommentForm()

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'comments': comments,
        'form': form,
    })


@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('main_page')
    else:
        form = ThreadForm()

    return render(request, 'forum/create_thread.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Активируем пользователя только после подтверждения
            user.save()
            send_confirmation_email(user, request)
            return HttpResponse("Письмо с подтверждением отправлено на вашу почту.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def confirm_email(request, uid, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Авторизация пользователя после подтверждения
        return redirect('main_page')
    else:
        return HttpResponse("Ссылка подтверждения недействительна.")