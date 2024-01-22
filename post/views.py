from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm


@login_required()
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        like = Like.objects.filter(user=request.user, post=post).exists()
        post.con = like
    return render(request, 'post/post_list.html', {'posts': posts})


@login_required()
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.filter(post=post)
    return render(request, 'post/post_detail.html', {'post': post,
                                                     'comments': comment})


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


@login_required
def like_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)

    like_exists = Like.objects.filter(user=user, post=post).exists()

    if like_exists:
        Like.objects.filter(user=user, post=post).delete()
    else:
        Like.objects.create(user=user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'post_list'))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=user, post=post, text=text)
            return redirect('post-list')

    return render(request, 'post/post-list.html', {'post': post})
