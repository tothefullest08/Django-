from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
# Create your views here.

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            # post_form.save()
        return redirect('posts:list')
    else:
        post_form = PostForm()
    return render(request, 'posts/create.htm', {'post_form':post_form})

def list(request):
    posts = Post.objects.order_by('-id').all()
    comment_form = CommentForm()
    return render(request, 'posts/list.htm', {'posts':posts, 'comment_form':comment_form})

def detail(request, post_id):
    post = get_object_or_404(Post, id= post_id)
    return render(request, 'posts/detail.htm', {'post': post})

def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        redirect('posts:list')

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
        return redirect('posts:list')
    
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/create.htm', {'post_form':post_form})

def delete(request, post_id):
    post  = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        redirect('posts:list')
        
    post.delete()
    return redirect('posts:list')

@require_POST
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
    return redirect('posts:list')

@require_http_methods(['POST', 'GET'])
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('posts:list')
    comment.delete()
    return redirect('posts:list')
