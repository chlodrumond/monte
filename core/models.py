from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os

def user_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f'user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100, help_text="Curso na PUC-Rio")
    altitude_points = models.IntegerField(default=0, help_text="Pontos de altitude conquistados")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.curso}"
    
    @property
    def current_mountain(self):
        """Retorna a montanha atual baseada nos pontos de altitude"""
        if self.altitude_points >= 1000:
            return "Everest"
        elif self.altitude_points >= 500:
            return "Kilimanjaro"
        elif self.altitude_points >= 200:
            return "Pico da Neblina"
        elif self.altitude_points >= 100:
            return "Pedra da Gávea"
        elif self.altitude_points >= 50:
            return "Pão de Açúcar"
        else:
            return "Morro da Urca"
    
    def add_altitude_points(self, points):
        """Adiciona pontos de altitude"""
        self.altitude_points += points
        self.save()

class Material(models.Model):
    TIPO_CHOICES = [
        ('resumo', 'Resumo'),
        ('apostila', 'Apostila'),
        ('prova', 'Prova'),
        ('exercicio', 'Exercício'),
        ('apresentacao', 'Apresentação'),
        ('artigo', 'Artigo'),
        ('outro', 'Outro'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(max_length=1000, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    materia = models.CharField(max_length=100)
    nivel_serie = models.CharField(max_length=50, help_text="Ex: 1º período, 2º ano, etc.")
    arquivo = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx'])]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    downloads = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.titulo} ({self.materia})"
    
    @property
    def file_size(self):
        """Retorna o tamanho do arquivo em MB"""
        try:
            return round(self.arquivo.size / (1024 * 1024), 2)
        except:
            return 0
    
    def increment_downloads(self):
        """Incrementa o contador de downloads"""
        self.downloads += 1
        self.save()

class Avaliacao(models.Model):
    NOTA_CHOICES = [
        (1, '1 - Muito Ruim'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='avaliacoes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=NOTA_CHOICES)
    comentario = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['material', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.material.titulo} - {self.nota}"

class Comentario(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.material.titulo}"

# Signals para adicionar pontos automaticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Material)
def add_upload_points(sender, instance, created, **kwargs):
    if created:
        # Adiciona 50 pontos por upload
        instance.user.userprofile.add_altitude_points(50)

@receiver(post_save, sender=Comentario)
def add_comment_points(sender, instance, created, **kwargs):
    if created:
        # Adiciona 10 pontos por comentário
        instance.user.userprofile.add_altitude_points(10)

@receiver(post_save, sender=Avaliacao)
def add_rating_points(sender, instance, created, **kwargs):
    if created:
        # Adiciona 5 pontos para quem recebe avaliação
        instance.material.user.userprofile.add_altitude_points(5)