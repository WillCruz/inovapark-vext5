from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('startups:home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'startups/login.html')

@login_required
def home_view(request):
    return render(request, 'startups/home.html')

def password_reset_view(request):
    # Apenas a interface por enquanto
    return render(request, 'startups/password_reset.html')

def logout_view(request):
    logout(request)
    return redirect('login')