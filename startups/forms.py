from django import forms
from .models import Startup, Pagamento
import datetime # <-- PASSO 1: IMPORTE A BIBLIOTECA DATETIME

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        # Adicione os novos campos à lista 'fields'
        fields = [
            'nome', 
            'cnpj', 
            'representante', 
            'email', 
            'telefone',
            'fase',
            'tipo_incubacao',             # <-- ADICIONADO
            'plataforma_tecnologica',   # <-- ADICIONADO
            'plano',                      # <-- ADICIONADO
        ]
        # Opcional: Adicione widgets para estilização
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'representante': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'fase': forms.Select(attrs={'class': 'form-select'}),
            'tipo_incubacao': forms.Select(attrs={'class': 'form-select'}),       # <-- ADICIONADO
            'plataforma_tecnologica': forms.TextInput(attrs={'class': 'form-control'}), # <-- ADICIONADO
            'plano': forms.Select(attrs={'class': 'form-select'}),                # <-- ADICIONADO
        }

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['rascunho_documentos', 'documentacao_pendente']
        widgets = {
            'rascunho_documentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'documentacao_pendente': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

class PagamentoForm(forms.ModelForm):
    data = forms.DateField(
        label="Data",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        initial=datetime.date.today,
        
    )

    class Meta:
        model = Pagamento
        fields = ['valor', 'status', 'data', 'descricao']
        
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Mensalidade, Consultoria...'}),
        }

class FaturamentoForm(forms.Form):
    valor_faturamento = forms.DecimalField(
        label="Valor do Faturamento R$", 
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    status = forms.ChoiceField(choices=Pagamento.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

class FinanceiroPendenteForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['financeiro_pendente']
        widgets = {
            'financeiro_pendente': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }