from django.db import models


class Startup(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome