from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return render(request, 'homepage/home.html')
    else:
        return render(request, 'homepage/index.html')

def userhome(request):
    return render(request, 'homepage/userhome.html')
