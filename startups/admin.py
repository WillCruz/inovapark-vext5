from django.contrib import admin
from .models import Startup, FaseIncubacao, ModeloIncubacao, PlanoIncubacao

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'cnpj',
        'representante',
        'email',
        'telefone',
        'ativo',
        'fase',
        'modelo_incubacao',
        'plano',
        'data_cadastro',
    )
    list_filter = (
        'ativo',
        'fase',
        'modelo_incubacao',
        'plano',
    )
    search_fields = (
        'nome',
        'cnpj',
        'representante',
        'email',
    )
    # Se quiser usar autocomplete (requer configuração de search_fields nas models relacionadas)
    autocomplete_fields = (
        'fase',
        'modelo_incubacao',
        'plano',
    )
    # Ou, se preferir um lookup simples
    raw_id_fields = (
        'fase',
        'modelo_incubacao',
        'plano',
    )

@admin.register(FaseIncubacao)
class FaseIncubacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(ModeloIncubacao)
class ModeloIncubacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(PlanoIncubacao)
class PlanoIncubacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
