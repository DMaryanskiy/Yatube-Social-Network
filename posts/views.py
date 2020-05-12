""" импортируем функции рендеринга и проверки наличия объекта в модели """
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import reverse

from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm

User = get_user_model()

@cache_page(20)
def index(request):
    """ Функция отображения главной страницы. При помощи паджинатора
    посты отображаются по 10 штук на страницу и сортируются от самого свежего
    к самому древнему """
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    form = CommentForm(request.POST)
    return render(
        request, "index.html", {
            "page": page,
            "paginator": paginator,
            "form" : form,
        }
    )

def group_posts(request, slug):
    """ создаем функцию отображения постов в конкретной группе
    будут отображены последние 10 постов, отсортированные по дате публикации
    и принадлежащие одной и той же группе. Для удобства используется паджинатор """
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    form = CommentForm(request.POST)
    return render(
        request, "group.html", {
            "group": group,
            "page": page,
            "paginator": paginator,
            "form" : form,
        }
    )

@login_required
def new_post(request):
    """ создаем функцию отправки формы на сервер,
    и если форма валидная, то пользователя возвращает
    на главную страницу """
    if request.method == "POST":
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")

        return render(request, "new_post.html", {"form": form,})

    form = PostForm()
    return render(request, "new_post.html", {"form": form,})

def profile(request, username):
    """ создаем функцию отображения страницы профиля,
    на которой отображаются посты определенного автора,
    отсортированные по дате публикации и разделенные по 10 штук
    на страницу паджинатором """
    user = request.user
    author = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=author)
    cnt = post.count()
    post_list = post.order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    form = CommentForm(request.POST)
    if user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=author)
    else:
        following = False
    return render(
        request, "profile.html", {
            "author": author,
            "cnt" : cnt,
            "post" : post,
            "page": page,
            "paginator" : paginator,
            "form" : form,
            "following" : following,
        }
    )

def post_view(request, username, post_id):
    """ создаем функцию отображения одного единственного поста
    путем перехода со страницы пользователя на сам этот пост """
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    cnt = Post.objects.filter(author=author).count()
    form = CommentForm(request.POST)
    comments = Comment.objects.filter(post=post).order_by("-created")
    return render(
        request, "post.html", {
            "post" : post,
            "author": author,
            "cnt" : cnt,
            "form" : form,
            "comments" : comments,
        }
    )

@login_required
def post_edit(request, username, post_id):
    """ функция отображения формы редактирования поста """
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect("post", username=request.user.username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)

    form = PostForm()
    return render(
        request, "new_post.html", {
            "form": form,
            "post": post,
        },
    )

def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)

@login_required
def add_comment(request, username, post_id):
    """ функция отображения формы заполнения комментариев """
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)
        
    form = CommentForm()
    return render(
        request, "comments.html", {
            "form" : form,
            "post" : post,
        }
    )

@login_required
def follow_index(request):
    follow = Follow.objects.filter(user=request.user)
    authors_list = follow.values_list("author")
    post_list = Post.objects.filter(author__in=authors_list).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    form = CommentForm(request.POST)
    return render(
        request, "follow.html", {
            "page": page,
            "paginator": paginator,
            "form" : form,
        }
    )

@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    exists = Follow.objects.filter(user=user, author=author).exists()
    if user != author and not exists:
        Follow.objects.create(user=user, author=author)
    return redirect("profile", username=author)

@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=user, author=author)
    follow.delete()
    return redirect("profile", username=username)
