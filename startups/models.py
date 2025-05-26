from django.db import models

class Startup(models.Model):
    nome = models.CharField(max_length=100)
    # outros campos que você precisar

    def __str__(self):
        return self.nome