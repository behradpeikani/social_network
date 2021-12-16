from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from .models import Post, Comment, Like
from account.models import Profile
from .forms import PostForm, EditPostForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
import redis
from django.conf import settings

# Create your views here.

@login_required
def posts_list(request):
    posts = Post.objects.filter(user__profile__followers__pk=request.user.pk)

    context = {"posts": posts}

    return render(request, 'posts/posts_list.html', context)

redis_con = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(is_reply=False, post=post)
    reply_form = ReplyForm()

    redis_con.hsetnx('post_views', str(post.id), 0)
    number_of_views = redis_con.hincrby('post_views', str(post.id))

    can_like = False
    if post.user_likes(request.user):
        can_like = True

    try:
        Like.objects.get(user=request.user, post_id=post_id)
        liked_this_post = True
    except:
        liked_this_post = False


    form = CommentForm(request.POST or None)        
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    context = {"post": post, "comments": comments, "reply_form": reply_form, "can_like": can_like,
     "form": form, "number_of_views": number_of_views, "liked_this_post": liked_this_post}
    
    return render(request, 'posts/post_detail.html', context)

@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        form = PostForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                messages.success(request, 'New post were added', 'success')
                return redirect('account:dashboard_view', user_id)
        else:
            form = PostForm()
        
        context = {"form": form}
        
        return render(request, 'posts/add_post.html', context)
    else:
        return redirect('posts:posts_list')

@login_required
def delete_post(request, user_id, post_id):
    if user_id == request.user.id:
        Post.objects.filter(id=post_id).delete()
        messages.success(request, 'Post deleted', 'success')
        return redirect('account:dashboard_view', user_id)
    else:
        return redirect('posts:posts_list')

@login_required
def edit_post(request, user_id, post_id):
    if user_id == request.user.id:
        post = get_object_or_404(Post, id=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post edited', 'success')
                return redirect('posts:post_detail', post_id)
        else:
            form = EditPostForm(instance=post)
            context = {"form": form}
        return render(request, 'posts/edit_post.html', context)
    else:
        return redirect('posts:posts_list')

@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST or None)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            form = ReplyForm()
    else:
        form = ReplyForm()
    return redirect('posts:post_detail', post.id)

@login_required
def like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like(user=request.user, post=post)
    like.save()
    return redirect('posts:post_detail', post.id)

@login_required
def unlike_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.get(user=request.user, post_id=post_id)
    like.delete()
    return redirect('posts:post_detail', post.id)



