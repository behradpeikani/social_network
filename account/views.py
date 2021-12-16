from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .decorators import login_excluded
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Profile
from posts.models import Post

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_excluded('posts:posts_list')
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name,
                 username=username, email=email, password=password)
            except:
                user = None

            if user != None:
                messages.success(request, 'Your account has been successfully created', 'success')
                return redirect('account:login_view')
            else:
                messages.info(request, 'Registration unseccessful! try again.', 'warning')

    context = {"form":form}

    return render(request, 'account/register_view.html', context)

@login_excluded('posts:posts_list')
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in')
                return redirect('posts:posts_list')
            else:
                return messages.error(request, 'Invalid username or password! try again.', 'warning')
    else:
        form = LoginForm()

    context = {"form":form}

    return render(request, 'account/login_view.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out', 'success')
    return redirect('account:login_view')

@login_required
def dashboard_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(user=user)

    followers = user.profile.followers.all()

    if len(followers) == 0:
        is_following = False

    for follower in followers:
        if follower == request.user:
            is_following = True
        else:
            is_following = False

    number_of_followers = len(followers)
    
    self_dash = False
    if request.user.pk == pk:
        self_dash = True
    
    context = {"user": user, "posts": posts, "self_dash": self_dash, "number_of_followers": number_of_followers, 
    "is_following": is_following}
    
    return render(request, 'account/dashboard_view.html', context)

@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, 'Profile edited', 'success')
            return redirect('account:dashboard_view', user.pk)
    else:
        form = ProfileForm(instance=user.profile, initial={'username': request.user.username})

    context = {"form": form}

    return render(request, 'account/edit_profile.html', context)

@login_required
def all_profiles(request):
    profiles = Profile.objects.all().exclude(user=request.user)

    context = {"profiles": profiles}

    return render(request, 'account/all_profiles.html', context)


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('account:dashboard_view', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('account:dashboard_view', pk=profile.pk)


class FollowersList(View):
    template_name = 'account/followers_list.html'
    model = Profile

    def get(self, request, pk, *args, **kwargs):
        profile = self.model.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {"followers": followers, "profile": profile}

        return render(request, self.template_name, context)