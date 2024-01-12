from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('view_profile')
    else:
        form = ProfileForm()

    return render(request, 'user/create_profile.html', {'form': form})


@login_required
def view_profile(request,pk):
    profile = Profile.objects.get(pk=pk)
    post = profile.user.post_set.all()
    return render(request, 'user/profile_detail.html', {'profile': profile,
                                                        'post': post})


@login_required
def edit_profile(request,pk):
    profile = Profile.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form,
                                                      'profile': profile})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('post-list')

    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
