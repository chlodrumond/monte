from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class MountainLevel(models.Model):
    """Representa os níveis de montanha no sistema de gamificação"""
    name = models.CharField(max_length=100, verbose_name="Nome da Montanha")
    min_altitude = models.IntegerField(verbose_name="Altitude Mínima")
    max_altitude = models.IntegerField(verbose_name="Altitude Máxima")
    description = models.TextField(blank=True, verbose_name="Descrição")
    image = models.ImageField(upload_to='mountains/', blank=True, null=True, verbose_name="Imagem")
    
    class Meta:
        verbose_name = "Nível de Montanha"
        verbose_name_plural = "Níveis de Montanha"
        ordering = ['min_altitude']
    
    def __str__(self):
        return f"{self.name} ({self.min_altitude}-{self.max_altitude}m)"


class UserProfile(models.Model):
    """Extensão do modelo de usuário com informações acadêmicas e de gamificação"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    curso = models.CharField(max_length=100, verbose_name="Curso")
    altitude_total = models.IntegerField(default=0, verbose_name="Altitude Total")
    montanha_atual = models.ForeignKey(
        MountainLevel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Montanha Atual"
    )
    montanhas_conquistadas = models.ManyToManyField(
        MountainLevel, 
        through='MountainAchievement', 
        related_name='conquistadores',
        verbose_name="Montanhas Conquistadas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.curso}"
    
    def add_altitude(self, points):
        """Adiciona pontos de altitude e verifica conquistas de montanha"""
        self.altitude_total += points
        self.save()
        self.check_mountain_achievements()
    
    def check_mountain_achievements(self):
        """Verifica e atualiza conquistas de montanha"""
        # Encontra a montanha atual baseada na altitude
        current_mountain = MountainLevel.objects.filter(
            min_altitude__lte=self.altitude_total,
            max_altitude__gte=self.altitude_total
        ).first()
        
        if current_mountain and current_mountain != self.montanha_atual:
            self.montanha_atual = current_mountain
            self.save()
            
            # Registra a conquista se ainda não foi registrada
            achievement, created = MountainAchievement.objects.get_or_create(
                user_profile=self,
                mountain=current_mountain,
                defaults={'achieved_at': timezone.now()}
            )
            
            return created  # Retorna True se é uma nova conquista
        return False


class MountainAchievement(models.Model):
    """Registro das conquistas de montanha dos usuários"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    mountain = models.ForeignKey(MountainLevel, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_profile', 'mountain']
        verbose_name = "Conquista de Montanha"
        verbose_name_plural = "Conquistas de Montanha"
        ordering = ['-achieved_at']
    
    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.mountain.name}"


class Material(models.Model):
    """Materiais acadêmicos compartilhados pelos usuários"""
    TIPO_CHOICES = [
        ('resumo', 'Resumo'),
        ('apostila', 'Apostila'),
        ('exercicios', 'Lista de Exercícios'),
        ('prova', 'Prova Antiga'),
        ('projeto', 'Projeto'),
        ('artigo', 'Artigo'),
        ('outros', 'Outros'),
    ]
    
    SERIE_CHOICES = [
        ('G1', 'G1 (1º Período)'),
        ('G2', 'G2 (2º Período)'),
        ('G3', 'G3 (3º Período)'),
        ('G4', 'G4 (4º Período)'),
        ('G5', 'G5 (5º Período)'),
        ('G6', 'G6 (6º Período)'),
        ('G7', 'G7 (7º Período)'),
        ('G8', 'G8 (8º Período)'),
        ('G9', 'G9 (9º Período)'),
        ('G10', 'G10 (10º Período)'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    materia = models.CharField(max_length=100, verbose_name="Matéria")
    serie = models.CharField(max_length=3, choices=SERIE_CHOICES, verbose_name="Período")
    arquivo = models.FileField(upload_to='materiais/', verbose_name="Arquivo")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name="Data de Upload")
    downloads = models.IntegerField(default=0, verbose_name="Downloads")
    aprovacoes = models.IntegerField(default=0, verbose_name="Aprovações")
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
    destaque = models.BooleanField(default=False, verbose_name="Material em Destaque")
    tags = models.CharField(max_length=500, blank=True, verbose_name="Tags (separadas por vírgula)")
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ['-data_upload']
    
    def __str__(self):
        return self.titulo
    
    def rating_medio(self):
        """Calcula a média das avaliações"""
        avaliacoes = self.avaliacao_set.all()
        if avaliacoes:
            return sum(a.nota for a in avaliacoes) / len(avaliacoes)
        return 0
    
    def total_avaliacoes(self):
        """Retorna o total de avaliações"""
        return self.avaliacao_set.count()
    
    def incrementar_visualizacao(self):
        """Incrementa o contador de visualizações"""
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])
    
    def calcular_popularidade(self):
        """Calcula score de popularidade baseado em visualizações, downloads e avaliações"""
        rating = self.rating_medio() or 0
        return (self.visualizacoes * 0.1) + (self.downloads * 0.5) + (rating * 2) + (self.total_avaliacoes() * 0.3)
    
    def get_tags_list(self):
        """Retorna lista de tags"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class Comentario(models.Model):
    """Comentários nos materiais"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    texto = models.TextField(verbose_name="Comentário")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data")
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Comentário de {self.autor.get_full_name()} em {self.material.titulo}"


class Avaliacao(models.Model):
    """Avaliações dos materiais (1-5 estrelas)"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material")
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Avaliador")
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Nota")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")
    
    class Meta:
        unique_together = ['material', 'avaliador']
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ['-data_avaliacao']
    
    def __str__(self):
        return f"Avaliação {self.nota}★ de {self.avaliador.get_full_name()}"


class Notificacao(models.Model):
    """Sistema de notificações para os usuários"""
    TIPO_CHOICES = [
        ('conquista', 'Nova Conquista'),
        ('comentario', 'Novo Comentário'),
        ('avaliacao', 'Nova Avaliação'),
        ('material', 'Novo Material'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensagem = models.TextField(verbose_name="Mensagem")
    lida = models.BooleanField(default=False, verbose_name="Lida")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data")
    
    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.get_full_name()}"


# Signal para criar automaticamente o perfil do usuário
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class SocialShare(models.Model):
    """Modelo para rastrear compartilhamentos sociais"""
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('email', 'Email'),
        ('link', 'Link Direto'),
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário")
    plataforma = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="Plataforma")
    data_compartilhamento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Compartilhamento")
    
    class Meta:
        verbose_name = "Compartilhamento Social"
        verbose_name_plural = "Compartilhamentos Sociais"
        ordering = ['-data_compartilhamento']
    
    def __str__(self):
        usuario_nome = self.usuario.get_full_name() if self.usuario else "Anônimo"
        return f"{usuario_nome} - {self.material.titulo} via {self.get_plataforma_display()}"


class MaterialFavorito(models.Model):
    """Materiais favoritados pelos usuários"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material")
    data_favoritado = models.DateTimeField(auto_now_add=True, verbose_name="Data Favoritado")
    
    class Meta:
        unique_together = ['usuario', 'material']
        verbose_name = "Material Favorito"
        verbose_name_plural = "Materiais Favoritos"
        ordering = ['-data_favoritado']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.material.titulo}"


class UserFollow(models.Model):
    """Sistema de seguir usuários"""
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo', verbose_name="Seguidor")
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores', verbose_name="Seguido")
    data_seguimento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Seguimento")

    class Meta:
        unique_together = ['seguidor', 'seguido']
        verbose_name = "Seguimento"
        verbose_name_plural = "Seguimentos"
        ordering = ['-data_seguimento']

    def __str__(self):
        return f"{self.seguidor.get_full_name()} segue {self.seguido.get_full_name()}"


class ChatRoom(models.Model):
    """Salas de chat entre usuários"""
    TIPO_CHOICES = [
        ('privado', 'Chat Privado'),
        ('grupo', 'Grupo de Estudo'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome da Sala", blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='privado', verbose_name="Tipo")
    participantes = models.ManyToManyField(User, verbose_name="Participantes")
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salas_criadas', verbose_name="Criador")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Sala de Chat"
        verbose_name_plural = "Salas de Chat"
        ordering = ['-data_criacao']

    def __str__(self):
        if self.nome:
            return self.nome
        elif self.tipo == 'privado':
            participantes = list(self.participantes.all()[:2])
            if len(participantes) == 2:
                return f"Chat: {participantes[0].get_full_name()} & {participantes[1].get_full_name()}"
        return f"Sala #{self.id}"

    def get_ultimo_mensagem(self):
        """Retorna a última mensagem da sala"""
        return self.mensagens.order_by('-data_envio').first()


class ChatMessage(models.Model):
    """Mensagens do chat"""
    sala = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='mensagens', verbose_name="Sala")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    conteudo = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    lida = models.BooleanField(default=False, verbose_name="Lida")

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['data_envio']

    def __str__(self):
        return f"{self.autor.get_full_name()}: {self.conteudo[:50]}..."