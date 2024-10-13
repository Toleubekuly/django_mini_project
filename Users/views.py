from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, ProfileEditForm
from .models import ProfileF, Follow
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Регистрация прошла успешно! Вы можете войти.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'Users/registration.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', username=username)
        else:
            return render(request, 'Users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'Users/login.html')

@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(ProfileF, user=user)
    return render(request, 'Users/profile.html', {
        'user': user,
        'profile': profile
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(ProfileF, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'Users/edit_profile.html', {'form': form})

@login_required
def follow_user(request, username):
    following_user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        if created:
            return JsonResponse({'message': f'You are now following {following_user.username}'})
        else:
            return JsonResponse({'message': f'You are already following {following_user.username}'})

@login_required
def unfollow_user(request, username):
    following_user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        follow = get_object_or_404(Follow, follower=request.user, following=following_user)
        follow.delete()
        return JsonResponse({'message': f'You have unfollowed {following_user.username}'})
