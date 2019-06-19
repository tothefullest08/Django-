from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .forms import CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.

def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
        return redirect('posts:list')

    else:
        signup_form = UserCreationForm()
    return render(request, 'accounts/signup.htm', {'signup_form':signup_form})

def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('posts:list')    
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.htm', {'login_form':login_form})

def logout(request):
    auth_logout(request)
    return redirect('posts:list')

def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    # people = get_object_or_404(settings.AUTH_USER_MODEL, username=username)

    return render(request, 'accounts/people.htm', {'people':people})

@login_required
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('accounts:people', request.user.username)
    
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/update.htm', {'user_change_form':user_change_form})

@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('posts:list')
    return render(request, 'accounts/delete.htm')

@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user =request.user, data = request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
        return redirect('accounts:people', request.user.username)
    

    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.htm', {'password_change_form': password_change_form})
