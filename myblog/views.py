from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from taggit.models import Tag
from .models import Post, Category, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm


def home(request):
    posts_list = Post.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myblog/index.html', {'page_obj': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    common_tags = Post.tags.most_common()[:10]
    last_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:5]

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.username = request.user
                comment.name = request.user.username
                comment.save()
                return redirect('post_detail', slug=post.slug)
        else:
            return redirect('login') # Гостей перекидываем на вход
    else:
        comment_form = CommentForm()

    return render(request, 'myblog/post_detail.html', {
        'post': post,
        'common_tags': common_tags,
        'last_posts': last_posts,
        'comment_form': comment_form
    })

def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()
    else:
        posts = []
    return render(request, 'myblog/search.html', {'posts': posts, 'query': query})


def contact(request):
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    f'От {name} | {subject}',
                    f'Сообщение от: {name}\nEmail: {from_email}\n\n{message}',
                    'poropororo.Hh@yandex.ru',  # <-- ТУТ ТВОЯ ПОЧТА (от кого)
                    ['poropororo.Hh@yandex.ru'],  # <-- ТУТ ТВОЯ ПОЧТА (кому)
                )
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return redirect('thanks')
    else:
        form = FeedBackForm()
    return render(request, 'myblog/contact.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                form.add_error(None, "Неправильный пароль или пользователь не существует")
    else:
        form = SignInForm()
    return render(request, 'myblog/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Аккаунт {user.username} создан!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'myblog/signup.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')


def thanks(request):
    return render(request, 'myblog/thanks.html')


def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, is_published=True)
    common_tags = Post.tags.most_common()[:10]
    return render(request, 'myblog/tag.html', {
        'tag': tag,
        'posts': posts,
        'common_tags': common_tags
    })


@staff_member_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        if title and slug and content and category_id:
            category = Category.objects.get(id=category_id)
            Post.objects.create(
                title=title, slug=slug, content=content,
                category=category, author=request.user, image=image
            )
            return redirect('home')
    categories = Category.objects.all()
    return render(request, 'myblog/add_post.html', {'categories': categories})


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        if title and slug:
            Category.objects.create(title=title, slug=slug)
            return redirect('add_post')
    return render(request, 'myblog/add_category.html')