from .models import Post
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm


# Create your views here.


@login_required()
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/post_list.html', {'posts': posts})


@login_required()
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_detail.html', {'post': post})


@login_required()
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('view_profile', pk=post.user.pk)
    else:
        form = PostForm()
        post = request.user.post_set.first()

    return render(request, 'post/post_form.html', {'form': form, 'post': post})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_form.html', {'form': form})


@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('view_profile', pk=post.user.pk)
    context = {'object': post}
    return render(request, 'post/delete_template.html', context)
