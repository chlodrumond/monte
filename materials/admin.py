from django.contrib import admin
from .models import (
    MountainLevel, UserProfile, Material, Comentario, 
    Avaliacao, Notificacao, MountainAchievement, SocialShare, MaterialFavorito
)


@admin.register(MountainLevel)
class MountainLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_altitude', 'max_altitude']
    ordering = ['min_altitude']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'curso', 'altitude_total', 'montanha_atual']
    list_filter = ['curso', 'montanha_atual']
    search_fields = ['user__username', 'user__email', 'curso']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'tipo', 'materia', 'serie', 'data_upload', 'downloads', 'visualizacoes', 'destaque']
    list_filter = ['tipo', 'serie', 'data_upload', 'destaque']
    search_fields = ['titulo', 'descricao', 'materia', 'autor__username', 'tags']
    date_hierarchy = 'data_upload'
    list_editable = ['destaque']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'material', 'data_criacao']
    list_filter = ['data_criacao']
    search_fields = ['texto', 'autor__username', 'material__titulo']


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['avaliador', 'material', 'nota', 'data_avaliacao']
    list_filter = ['nota', 'data_avaliacao']


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'titulo', 'lida', 'data_criacao']
    list_filter = ['tipo', 'lida', 'data_criacao']
    search_fields = ['titulo', 'mensagem', 'usuario__username']


@admin.register(MountainAchievement)
class MountainAchievementAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'mountain', 'achieved_at']
    list_filter = ['mountain', 'achieved_at']


@admin.register(SocialShare)
class SocialShareAdmin(admin.ModelAdmin):
    list_display = ['material', 'usuario', 'plataforma', 'data_compartilhamento']
    list_filter = ['plataforma', 'data_compartilhamento']
    search_fields = ['material__titulo', 'usuario__username']


@admin.register(MaterialFavorito)
class MaterialFavoritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'material', 'data_favoritado']
    list_filter = ['data_favoritado']
    search_fields = ['usuario__username', 'material__titulo']