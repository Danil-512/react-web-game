from django.shortcuts import render

# Create your views here.

def index_page(request):
    i = 1
    return render(request, 'index.html')

def about_page(request):
    i = 1
    return render(request, 'index.html')