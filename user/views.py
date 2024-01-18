from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


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
def view_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    post = profile.user.post_set.all()

    followers_count = Follow.objects.filter(following=profile.user).count()
    following_count = Follow.objects.filter(follower=profile.user).count()

    follow_exists = Follow.objects.filter(follower=request.user,
                                          following=profile.user).exists()

    return render(request, 'user/profile_detail.html', {'profile': profile,
                                                        'post': post,
                                                        'follow_exists':
                                                            follow_exists,
                                                        'followers_count': followers_count,
                                                        'following_count': following_count,
                                                        })


@login_required
def edit_profile(request, pk):
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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-list')
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})


def all_users(request):
    user = Profile.objects.all()
    if request.method == "POST":
        data = request.POST.get("query")
        user = Profile.objects.filter(name__icontains=data)
        print(user)

    return render(request, 'user/all_users.html', {'users': user})


@login_required
def follow_profile(request, pk):
    user = request.user
    following_user = get_object_or_404(User, pk=pk)
    follow_exists = Follow.objects.filter(follower=user,
                                          following=following_user).exists()

    if follow_exists:
        Follow.objects.filter(follower=user, following=following_user).delete()
        follow_exists = False
    else:
        Follow.objects.create(follower=user, following=following_user)
        follow_exists = True

    return redirect(request.META.get('HTTP_REFERER', 'profile_detail'))
