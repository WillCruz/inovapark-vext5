from django.contrib import admin
from .models import Startup

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'cnpj', 'representante')
    list_filter = ('ativo',)
