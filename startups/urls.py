from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'startups'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/fases/', views.fases_kanban_view, name='fases_kanban'),

    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    path('esqueci-senha/', auth_views.PasswordResetView.as_view(
        template_name='startups/password_reset_form.html'
    ), name='password_reset'),

    path('senha-enviada/', auth_views.PasswordResetDoneView.as_view(
        template_name='startups/password_reset_done.html'
    ), name='password_reset_done'),

    path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='startups/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('senha-redefinida/', auth_views.PasswordResetCompleteView.as_view(
        template_name='startups/password_reset_complete.html'
    ), name='password_reset_complete'),    
    # STARTUPS
    path('', views.listar_startups, name='listar_startups'),
    path('nova/', views.cadastrar_startup, name='cadastrar_startup'),
    path('<int:pk>/editar/', views.editar_startup, name='editar_startup'),
    path('<int:pk>/deletar/', views.deletar_startup, name='deletar_startup'),
    
    path('startup/<int:startup_id>/avancar-fase/', views.avancar_fase_view, name='avancar_fase'),
    path('startup/<int:startup_id>/documentos/', views.documentos_view, name='documentos_startup'),

    path('startup/<int:startup_id>/financeiro/', views.financeiro_view, name='financeiro_startup'),
    path('startup/<int:startup_id>/adicionar-pagamento/', views.adicionar_pagamento_view, name='adicionar_pagamento'),
    path('startup/<int:startup_id>/calcular-faturamento/', views.calcular_faturamento_view, name='calcular_faturamento'),
    path('pagamento/<int:pagamento_id>/editar/', views.editar_pagamento_view, name='editar_pagamento'),
    path('pagamento/<int:pagamento_id>/excluir/', views.excluir_pagamento_view, name='excluir_pagamento'),
]
