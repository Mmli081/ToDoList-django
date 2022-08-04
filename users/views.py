from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import AuthenticationForm
from django.contrib.auth import logout, login as login_dj, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


# Create your views here.

@login_required(login_url='login')
def index(request):
    return HttpResponse(f"Hello {request.user.username}. You're at the users index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_dj(request, user)
                return redirect('index') #TODO
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html' , {'form': form})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')