from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Material, Avaliacao, Comentario

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['curso', 'altitude_points']

# Extend UserAdmin to include UserProfile
class ExtendedUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'materia', 'user', 'created_at', 'downloads']
    list_filter = ['tipo', 'materia', 'created_at']
    search_fields = ['titulo', 'descricao', 'materia']
    readonly_fields = ['downloads', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'user')
        }),
        ('Categorização', {
            'fields': ('tipo', 'materia', 'nivel_serie')
        }),
        ('Arquivo', {
            'fields': ('arquivo',)
        }),
        ('Estatísticas', {
            'fields': ('downloads', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'nota', 'created_at']
    list_filter = ['nota', 'created_at']
    search_fields = ['material__titulo', 'user__username', 'comentario']
    ordering = ['-created_at']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'texto_truncado', 'created_at']
    list_filter = ['created_at']
    search_fields = ['material__titulo', 'user__username', 'texto']
    ordering = ['-created_at']
    
    def texto_truncado(self, obj):
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_truncado.short_description = 'Comentário'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'curso', 'altitude_points', 'current_mountain', 'created_at']
    list_filter = ['curso', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'curso']
    readonly_fields = ['created_at', 'updated_at', 'current_mountain']
    ordering = ['-altitude_points']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Acadêmicas', {
            'fields': ('curso',)
        }),
        ('Gamificação', {
            'fields': ('altitude_points', 'current_mountain')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Customize admin site headers
admin.site.site_header = "Monte - Administração"
admin.site.site_title = "Monte Admin"
admin.site.index_title = "Painel de Administração da Plataforma Monte"