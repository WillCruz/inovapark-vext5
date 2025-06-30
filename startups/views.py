from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

from .models import Startup, FaseIncubacao
from .forms import StartupForm


# Tela inicial com painel e métricas
@login_required
def home_view(request):
    total_startups = Startup.objects.count()
    startups_ativas = Startup.objects.filter(ativo=True).count()
    startups_inativas = Startup.objects.filter(ativo=False).count()
    ultimas_startups = Startup.objects.order_by('-data_cadastro')[:5]

    context = {
        'total_startups': total_startups,
        'startups_ativas': startups_ativas,
        'startups_inativas': startups_inativas,
        'ultimas_startups': ultimas_startups,
    }
    return render(request, 'startups/home.html', context)


# Lista de startups com botão de ações
@login_required
def listar_startups(request):
    startups = Startup.objects.all().order_by('-data_cadastro')
    return render(request, 'startups/listar_startups.html', {'startups': startups})


# Cadastro de nova startup
@login_required
def cadastrar_startup(request):
    if request.method == 'POST':
        form = StartupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Startup cadastrada com sucesso.')
            return redirect('startups:listar_startups')
    else:
        form = StartupForm()
    return render(request, 'startups/cadastrar_startup.html', {'form': form})


# Edição de uma startup
@login_required
def editar_startup(request, id):
    startup = get_object_or_404(Startup, id=id)
    if request.method == 'POST':
        form = StartupForm(request.POST, instance=startup)
        if form.is_valid():
            form.save()
            messages.success(request, 'Startup atualizada com sucesso.')
            return redirect('startups:listar_startups')
    else:
        form = StartupForm(instance=startup)
    return render(request, 'startups/editar_startup.html', {
        'form': form,
        'startup': startup
    })


# Exclusão de uma startup
@login_required
def deletar_startup(request, id):
    startup = get_object_or_404(Startup, id=id)
    if request.method == 'POST':
        startup.delete()
        messages.success(request, 'Startup deletada com sucesso.')
        return redirect('startups:listar_startups')
    return render(request, 'startups/deletar_startup.html', {'startup': startup})


# Visualização detalhada
@login_required
def detalhar_startup(request, id):
    startup = get_object_or_404(Startup, id=id)
    return render(request, 'startups/detalhar_startup.html', {'startup': startup})


# Autenticação (login/logout)
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('startups:home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'startups/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('startups:login')


# Kanban de fases de incubação
@login_required
def kanban_fases(request):
    fases = FaseIncubacao.objects.all().prefetch_related('startups')
    return render(request, 'startups/kanban_fases.html', {'fases': fases})


# Atualiza a fase de uma startup via AJAX
@require_POST
@csrf_exempt
def update_startup_fase(request):
    data = json.loads(request.body)
    s = Startup.objects.get(pk=data['id'])
    old = s.fase_id
    new = int(data['fase'])
    print(f"🚧 Startup#{s.id} fase antiga={old}")
    s.fase_id = new
    s.save()
    # Recarregar do DB pra garantir
    s.refresh_from_db()
    print(f"✔️ Startup#{s.id} fase agora={s.fase_id}")
    return JsonResponse({'success': True})