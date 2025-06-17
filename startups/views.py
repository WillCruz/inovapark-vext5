from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Startup
from .forms import StartupForm
from django.contrib.auth.decorators import login_required
##############################################################################################################
# LOGIN
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

def logout_view(request):
    logout(request)
    return redirect('startups:login')

##############################################################################################################
# STARTUPS

# Listar startups
@login_required
def listar_startups(request):
    startups = Startup.objects.all()
    return render(request, 'startups/listar_startups.html', {'startups': startups})

# Cadastrar nova startup
@login_required
def cadastrar_startup(request):
    if request.method == 'POST':
        form = StartupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('startups:listar_startups')
    else:
        form = StartupForm()
    return render(request, 'startups/cadastrar_startup.html', {'form': form})

# Editar startup existente
@login_required
def editar_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        form = StartupForm(request.POST, instance=startup)
        if form.is_valid():
            form.save()
            return redirect('startups:listar_startups')
    else:
        form = StartupForm(instance=startup)
    return render(request, 'startups/editar_startup.html', {'form': form, 'startup': startup})

# Deletar startup
@login_required
def deletar_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        startup.delete()
        return redirect('startups:listar_startups')
    return render(request, 'startups/deletar_startup.html', {'startup': startup})

##############################################################################################################
