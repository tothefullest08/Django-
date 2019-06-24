from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Image
from .forms import PostForm, CommentForm, ImageFormSet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from itertools import chain
# Create your views here.

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            with transaction.atomic():
                post.save()
                image_formset.instance = post
                image_formset.save()
                return redirect('posts:list')
    else:
        post_form = PostForm()
        image_formset = ImageFormSet()
    return render(request, 'posts/create.htm', {
                                        'post_form':post_form,
                                        'image_formset':image_formset
                                        })

def list(request):
    # followings = request.user.followings.values_list('id', flat=True)
    followings = request.user.followings.all()
    followings = chain(followings, [request.user])

    posts = Post.objects.filter(user__in=followings).order_by('id')
    comment_form = CommentForm()
    return render(request, 'posts/list.htm', {'posts':posts, 'comment_form':comment_form})

def explore(request):
    posts = Post.objects.all()
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
        post_form = PostForm(request.POST, instance=post)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=post)
        if post_form.is_valid() and image_formset.is_valid():
            post_form.save()
            image_formset.save()
        return redirect('posts:list')
    
    else:
        post_form = PostForm(instance=post)
        image_formset = ImageFormSet(instance=post)
    return render(request, 'posts/create.htm', {
                                    'post_form':post_form,
                                    'image_formset':image_formset,
                                    })

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

def comment_update(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return redirect('posts:list')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
        return redirect('posts:list')
    
    else:
        comment_form = CommentForm(instance=comment)
        return render(request, 'posts/comment_update.htm', {'comment_form':comment_form})

def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')

