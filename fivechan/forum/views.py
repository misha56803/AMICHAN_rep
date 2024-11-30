from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm

def main_page(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'forum/main_page.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = thread.comments.all().order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = CommentForm()

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'comments': comments, 'form': form})

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