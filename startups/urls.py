from django.urls import path
from . import views

app_name = 'startups'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('', views.listar_startups, name='listar_startups'),
    path('cadastrar/', views.cadastrar_startup, name='cadastrar_startup'),
    path('editar/<int:id>/', views.editar_startup, name='editar_startup'),
    path('excluir/<int:id>/', views.deletar_startup, name='excluir_startup'),
    path('detalhar/<int:id>/', views.detalhar_startup, name='detalhar_startup'),
    path('kanban-fases/', views.kanban_fases, name='kanban_fases'),
    path('kanban-fases/update/', views.update_startup_fase, name='update_startup_fase'),

]