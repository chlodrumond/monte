from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('upload/', views.upload_material, name='upload_material'),
    path('buscar/', views.buscar_materiais, name='buscar_materiais'),
    path('material/<int:material_id>/', views.detalhe_material, name='detalhe_material'),
    path('download/<int:material_id>/', views.download_material, name='download_material'),
    path('notificacao/<int:notificacao_id>/lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('ranking/', views.ranking_usuarios, name='ranking_usuarios'),
]