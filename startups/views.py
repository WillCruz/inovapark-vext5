import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST # type: ignore
from .models import Startup
from .forms import Pagamento, StartupForm, DocumentosForm, PagamentoForm, FaturamentoForm, FinanceiroPendenteForm
from decimal import Decimal # Importe o tipo Decimal para cálculos precisos

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




@login_required
def fases_kanban_view(request):
    """
    View que renderiza a página do Kanban de forma otimizada.
    """
    todas_startups = Startup.objects.filter(ativo=True).order_by('nome')
    
    startups_por_fase = {}
    for startup in todas_startups:
        startups_por_fase.setdefault(startup.fase, []).append(startup)
        
    fases_ordenadas = []
    for fase_id, fase_nome in Startup.FASES_CHOICES:
        fases_ordenadas.append({
            'id': fase_id,
            'nome': fase_nome,
            'startups': startups_por_fase.get(fase_id, []) 
        })
        
    context = {
        'fases_ordenadas': fases_ordenadas,
    }
    return render(request, 'startups/fases_kanban.html', context)

@require_POST
def update_startup_fase(request):
    """
    View de API para atualizar a fase de uma startup.
    """
    try:
        data = json.loads(request.body)
        startup_id = data.get('startup_id')
        nova_fase = data.get('nova_fase')
        
        if not startup_id or not nova_fase:
            return JsonResponse({'status': 'error', 'message': 'Dados incompletos.'}, status=400)

        startup = Startup.objects.get(id=startup_id)
        startup.fase = nova_fase
        startup.save()
        
        return JsonResponse({'status': 'success', 'message': f'Fase da {startup.nome} atualizada.'})

    except Startup.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Startup não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@login_required # Garante que apenas usuários logados podem avançar a fase
def avancar_fase_view(request, startup_id):
    """
    Encontra uma startup pelo seu ID e avança sua fase para a próxima na sequência.
    """
    if request.method == 'POST':
        try:
            startup = Startup.objects.get(id=startup_id)
            
            # Pega a lista de fases (apenas os IDs)
            lista_de_fases = [fase[0] for fase in Startup.FASES_CHOICES]
            
            # Encontra o índice da fase atual
            try:
                indice_atual = lista_de_fases.index(startup.fase)
            except ValueError:
                # Caso a fase atual não esteja na lista, não faz nada
                return redirect('startups:fases_kanban')

            # Verifica se não está na última fase
            if indice_atual < len(lista_de_fases) - 1:
                # Pega o ID da próxima fase
                proxima_fase = lista_de_fases[indice_atual + 1]
                startup.fase = proxima_fase
                startup.save()
                messages.success(request, f'A startup "{startup.nome}" avançou para a fase de {startup.get_fase_display()}.')
            else:
                messages.info(request, f'A startup "{startup.nome}" já está na fase final.')

        except Startup.DoesNotExist:
            messages.error(request, 'Startup não encontrada.')

    # Redireciona de volta para a página do Kanban após a ação
    return redirect('startups:fases_kanban')

@login_required
def documentos_view(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    
    if request.method == 'POST':
        # Esta linha é crucial: ela associa os dados enviados com a startup existente
        form = DocumentosForm(request.POST, instance=startup)
        if form.is_valid():
            form.save() # Esta linha salva as alterações no banco de dados
            messages.success(request, 'Alterações nos documentos salvas com sucesso!')
            return redirect('startups:documentos_startup', startup_id=startup.id)
    else:
        form = DocumentosForm(instance=startup)
        
    context = {
        'form': form,
        'startup': startup
    }
    return render(request, 'startups/documentos_startup.html', context)


# VIEW PRINCIPAL FINANCEIRA
@login_required
def financeiro_view(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    pagamentos = startup.pagamentos.all() # Pega todos os pagamentos relacionados a esta startup
    
    if request.method == 'POST':
        form_pendente = FinanceiroPendenteForm(request.POST, instance=startup)
        if form_pendente.is_valid():
            form_pendente.save()
            return redirect('startups:financeiro_startup', startup_id=startup.id)
    else:
        form_pendente = FinanceiroPendenteForm(instance=startup)

    context = {
        'startup': startup,
        'pagamentos': pagamentos,
        'form_pendente': form_pendente,
    }
    return render(request, 'startups/financeiro_startup.html', context)

# VIEW PARA ADICIONAR UM PAGAMENTO MANUAL
@login_required
def adicionar_pagamento_view(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False) # Não salva no banco ainda
            pagamento.startup = startup # Associa o pagamento à startup correta
            pagamento.save() # Agora salva
            messages.success(request, 'Pagamento adicionado com sucesso!')
            return redirect('startups:financeiro_startup', startup_id=startup.id)
    else:
        form = PagamentoForm()
    
    return render(request, 'startups/generic_form.html', {'form': form, 'titulo': 'Adicionar Pagamento'})

# VIEW PARA CALCULAR FATURAMENTO E CRIAR PAGAMENTO
@login_required
def calcular_faturamento_view(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == 'POST':
        form = FaturamentoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            valor_faturamento = dados['valor_faturamento']
            
            # Cálculo de 1.5%
            valor_calculado = valor_faturamento * Decimal('0.015')

            # Cria um novo registro de Pagamento com os dados calculados
            Pagamento.objects.create(
                startup=startup,
                valor=valor_calculado,
                status=dados['status'],
                data=dados['data'],
                descricao=f"Faturamento sobre R$ {valor_faturamento}"
            )
            messages.success(request, 'Pagamento de faturamento calculado e registrado com sucesso!')
            return redirect('startups:financeiro_startup', startup_id=startup.id)
    else:
        form = FaturamentoForm()

    return render(request, 'startups/generic_form.html', {'form': form, 'titulo': 'Calcular Faturamento'})

@login_required
def editar_pagamento_view(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    startup_id = pagamento.startup.id

    # --- INÍCIO DA DEPURAÇÃO E CORREÇÃO ---

    # Para depuração: vamos imprimir no terminal o que está vindo do banco
    print(f"DEBUG: Editando pagamento ID {pagamento.id}, Data do banco: {pagamento.data}, Tipo do dado: {type(pagamento.data)}")

    if request.method == 'POST':
        # A lógica de salvar continua a mesma
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('startups:financeiro_startup', startup_id=startup_id)
    else:
        # CORREÇÃO FORÇADA: Em vez de confiar no 'instance', vamos criar um dicionário
        # com os dados e formatar a data explicitamente.
        initial_data = {
            'valor': pagamento.valor,
            'status': pagamento.status,
            'data': pagamento.data.strftime('%Y-%m-%d'), # Formatação explícita para o formato que o HTML precisa
            'descricao': pagamento.descricao
        }
        # Criamos o formulário passando os dados iniciais manualmente
        form = PagamentoForm(initial=initial_data)
    
    # --- FIM DA DEPURAÇÃO E CORREÇÃO ---
    
    return render(request, 'startups/generic_form.html', {'form': form, 'titulo': f'Editar Pagamento de {pagamento.startup.nome}'})


# --- NOVA VIEW PARA EXCLUIR UM PAGAMENTO ---
@login_required
def excluir_pagamento_view(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    startup_id = pagamento.startup.id # Guarda o ID para o redirecionamento

    # A exclusão só acontece se o método for POST, para segurança
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Registro de pagamento excluído com sucesso.')
    
    # Após excluir (ou se o acesso for GET), volta para a página financeira
    return redirect('startups:financeiro_startup', startup_id=startup_id)