from django.db import models

class Startup(models.Model):
    # Definindo as fases como constantes para reutilização
    FASE_PRE_INCUBACAO = 'pre-incubacao'
    FASE_IMPLANTACAO = 'implantacao'
    FASE_CRESCIMENTO = 'crescimento'
    FASE_CONSOLIDACAO = 'consolidacao'
    FASE_GRADUACAO = 'graduacao'

    FASES_CHOICES = [
        (FASE_PRE_INCUBACAO, 'Pré-incubação'),
        (FASE_IMPLANTACAO, 'Implantação'),
        (FASE_CRESCIMENTO, 'Crescimento'),
        (FASE_CONSOLIDACAO, 'Consolidação'),
        (FASE_GRADUACAO, 'Graduação'),
    ]
    TIPO_RESIDENTE = 'residente'
    TIPO_NAO_RESIDENTE = 'nao_residente'
    TIPO_INCUBACAO_CHOICES = [
        (TIPO_RESIDENTE, 'Residente'),
        (TIPO_NAO_RESIDENTE, 'Não Residente'),
    ]

    # Opções para Plano
    PLANO_START = 'start'
    PLANO_GROW = 'grow'
    PLANO_CHOICES = [
        (PLANO_START, 'Start'),
        (PLANO_GROW, 'Grow'),
    ]

    tipo_incubacao = models.CharField(
        max_length=20,
        choices=TIPO_INCUBACAO_CHOICES,
        default=TIPO_RESIDENTE,
        verbose_name="Tipo de Incubação"
    )
    plataforma_tecnologica = models.CharField(
        max_length=255,
        blank=True, # Torna o campo opcional
        verbose_name="Plataforma Tecnológica"
    )
    plano = models.CharField(
        max_length=10,
        choices=PLANO_CHOICES,
        default=PLANO_START,
        verbose_name="Plano"
    )
    # ... seus campos existentes (id, nome, cnpj, etc.) ...
    nome = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name="CNPJ")
    representante = models.CharField(max_length=255, verbose_name="Representante Legal")
    email = models.EmailField(max_length=254, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativa")

    # NOVO CAMPO ADICIONADO AQUI
    fase = models.CharField(
        max_length=50,
        choices=FASES_CHOICES,
        default=FASE_PRE_INCUBACAO, # Define a fase padrão para novas startups
        verbose_name="Fase Atual"
    )

    rascunho_documentos = models.TextField(
        blank=True, # Permite que o campo fique em branco
        null=True,
        verbose_name="Rascunho de Documentos"
    )
    documentacao_pendente = models.BooleanField(
        default=False, # Por padrão, a documentação não está pendente
        verbose_name="Documentação Pendente"
    )

    # --- NOVO CAMPO PARA PENDÊNCIA FINANCEIRA ---
    financeiro_pendente = models.BooleanField(
        default=False,
        verbose_name="Financeiro Pendente"
    )

    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
    
class Pagamento(models.Model):
    STATUS_PAGO = 'pago'
    STATUS_PENDENTE = 'pendente'
    STATUS_CHOICES = [
        (STATUS_PAGO, 'Pago'),
        (STATUS_PENDENTE, 'Pendente'),
    ]

    startup = models.ForeignKey(
        Startup, 
        on_delete=models.CASCADE, # Se a startup for deletada, seus pagamentos também serão
        related_name='pagamentos',
        verbose_name="Startup"
    )
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Valor R$"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name="Status"
    )
    data = models.DateField(verbose_name="Data")
    descricao = models.CharField(max_length=255, blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data'] # Ordena os pagamentos do mais recente para o mais antigo

    def __str__(self):
        return f'{self.startup.nome} - R$ {self.valor} em {self.data.strftime("%d/%m/%Y")}'