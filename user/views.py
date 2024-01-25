from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, \
    TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Profile, Follow
from .forms import ProfileForm


class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/create_profile.html'
    success_url = reverse_lazy('view_profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ViewProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.user.post_set.all()
        context['followers_count'] = Follow.objects.filter(
            following=self.object.user).count()
        context['following_count'] = Follow.objects.filter(
            follower=self.object.user).count()
        context['follow_exists'] = Follow.objects.filter(
            follower=self.request.user, following=self.object.user).exists()
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.object.pk})


class RegisterUserView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AllUsersView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'user/all_users.html'
    context_object_name = 'users'

    def post(self, request, *args, **kwargs):
        data = self.request.POST.get("query")
        self.object_list = self.model.objects.filter(name__icontains=data)
        return self.render_to_response(self.get_context_data())


class FollowProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile_detail.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        following_user = get_object_or_404(User, pk=self.kwargs['pk'])
        follow_exists = Follow.objects.filter(follower=user,
                                              following=following_user).exists()

        if follow_exists:
            Follow.objects.filter(follower=user,
                                  following=following_user).delete()
        else:
            Follow.objects.create(follower=user, following=following_user)

        return redirect(
            self.request.META.get('HTTP_REFERER', 'profile_detail'))
