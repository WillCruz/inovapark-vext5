from django.db import models

class FaseIncubacao(models.Model):
    nome = models.CharField(
        max_length=50,
        verbose_name="Fase de Incubação",
        unique=True
    )

    class Meta:
        verbose_name = "Fase de Incubação"
        verbose_name_plural = "Fases de Incubação"

    def __str__(self):
        return self.nome

class ModeloIncubacao(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class PlanoIncubacao(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome} - {self.descricao}"    

class Startup(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True, null=True, blank=True)
    representante = models.CharField(max_length=255, verbose_name="Representante Legal")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativa")
    fase = models.ForeignKey(
        FaseIncubacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="startups",
        verbose_name="Fase de Incubação"
    )
    modelo_incubacao = models.ForeignKey(ModeloIncubacao, on_delete=models.SET_NULL, null=True, blank=True)
    plano = models.ForeignKey(PlanoIncubacao, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    

