from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404
@login_required
def home(request):
    posts = Post.objects.all()
    return render(request,"home.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Post.objects.create(
            title=title,
            content=content,
            user=request.user
        )

        return redirect("home")

    return render(request, "create_post.html")

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id,user=request.user)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("home")

    return render(request, "edit_post.html", {"post": post})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {'post': post})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        User.objects.create_user(username=username, password=password)
        return redirect("login")
    
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request,user)
            return redirect("home")
        
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

