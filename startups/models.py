from django.db import models

class Startup(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True, null=True, blank=True)
    representante = models.CharField(max_length=255, verbose_name="Representante Legal")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"
        ordering = ['nome']

    def __str__(self):
        return self.nome