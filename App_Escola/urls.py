from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('abre_cadastro', views.abre_cadastro, name='abre_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma_nova', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('ver_atividades/<int:pk>', views.ver_atividades, name='ver_atividades'),
    path('delete_turma/<int:pk>', views.delete_turma, name='delete_turma'),
    path('delete_atividade/<int:pk>', views.delete_atividade, name='delete_atividade'),
    path('salvar_atividade_nova/<int:pk>', views.salvar_atividade_nova, name='salvar_atividade_nova'),
]
