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
    
    # Novos recursos
    path('material/<int:material_id>/favoritar/', views.favoritar_material, name='favoritar_material'),
    path('favoritos/', views.meus_favoritos, name='meus_favoritos'),
    path('material/<int:material_id>/compartilhar/<str:plataforma>/', views.compartilhar_material, name='compartilhar_material'),
    path('populares/', views.materiais_populares, name='materiais_populares'),
    path('destaque/', views.materiais_destaque, name='materiais_destaque'),
    path('notificacoes/', views.notificacoes_usuario, name='notificacoes_usuario'),
]