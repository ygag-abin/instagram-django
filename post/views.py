from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
    DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Post, Like, Comment
from .forms import PostForm


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        for post in context['posts']:
            like = Like.objects.filter(user=user, post=post).exists()
            post.con = like

        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.object.user.pk})


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/delete_template.html'

    def get_success_url(self):
        return reverse_lazy('view_profile',
                            kwargs={'pk': self.get_object().user.pk})


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        like_exists = Like.objects.filter(user=user, post=post).exists()

        if like_exists:
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)

        return redirect(request.META.get('HTTP_REFERER', 'post_list'))


class AddCommentView(LoginRequiredMixin, View):
    template_name = 'post/post_list.html'

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        text = request.POST.get('text')

        if text:
            Comment.objects.create(user=user, post=post, text=text)
            return redirect('post-list')

        return render(request, self.template_name, {'post': post})
