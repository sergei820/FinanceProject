from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def index(request):
    return render(request, 'posts/posts.html')

def post(request):
    return render(request, 'posts/post.html')

def search(request):
    return render(request, 'posts/search.html')
