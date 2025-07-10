from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .models import (
    Material, Comentario, Avaliacao, UserProfile, 
    MountainLevel, Notificacao, MountainAchievement
)
from .forms import (
    CustomUserCreationForm, CustomLoginForm, MaterialForm,
    ComentarioForm, AvaliacaoForm, BuscaForm
)


def index(request):
    """Homepage com informações da plataforma"""
    # Estatísticas para mostrar na homepage
    total_materiais = Material.objects.count()
    total_usuarios = User.objects.count()
    materiais_recentes = Material.objects.select_related('autor').order_by('-data_upload')[:3]
    
    context = {
        'total_materiais': total_materiais,
        'total_usuarios': total_usuarios,
        'materiais_recentes': materiais_recentes,
    }
    return render(request, 'index.html', context)


def custom_login(request):
    """View personalizada de login com validação de email PUC-Rio"""
    if request.user.is_authenticated:
        return redirect('perfil')
    
    form = CustomLoginForm()
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Bem-vindo de volta, {user.get_full_name()}!')
                    return redirect('perfil')
                else:
                    messages.error(request, 'Senha incorreta.')
            except User.DoesNotExist:
                messages.error(request, 'Email não encontrado.')
    
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    """Cadastro de usuários com validação de email PUC-Rio"""
    if request.user.is_authenticated:
        return redirect('perfil')
    
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Faça login para continuar.')
            return redirect('login')
    
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def perfil(request):
    """Perfil do usuário com informações de progresso e montanhas"""
    profile = request.user.profile
    
    # Materiais do usuário
    materiais_usuario = Material.objects.filter(autor=request.user).order_by('-data_upload')[:5]
    
    # Notificações não lidas
    notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)[:5]
    
    # Conquistas de montanhas
    conquistas = MountainAchievement.objects.filter(user_profile=profile).order_by('-achieved_at')
    
    # Progresso atual (porcentagem para próxima montanha)
    progresso = 0
    if profile.montanha_atual:
        range_atual = profile.montanha_atual.max_altitude - profile.montanha_atual.min_altitude
        progresso_atual = profile.altitude_total - profile.montanha_atual.min_altitude
        progresso = (progresso_atual / range_atual) * 100 if range_atual > 0 else 100
    
    context = {
        'profile': profile,
        'materiais_usuario': materiais_usuario,
        'notificacoes': notificacoes,
        'conquistas': conquistas,
        'progresso': min(progresso, 100),
    }
    return render(request, 'materials/perfil.html', context)


@login_required
def upload_material(request):
    """Upload de materiais acadêmicos"""
    form = MaterialForm()
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.autor = request.user
            material.save()
            
            # Adicionar pontos de altitude (+50m por upload)
            request.user.profile.add_altitude(50)
            
            # Verificar se conquistou nova montanha
            nova_conquista = request.user.profile.check_mountain_achievements()
            if nova_conquista:
                messages.success(
                    request, 
                    f'Material enviado! Você conquistou a montanha {request.user.profile.montanha_atual.name}!'
                )
                # Criar notificação
                Notificacao.objects.create(
                    usuario=request.user,
                    tipo='conquista',
                    titulo='Nova Montanha Conquistada!',
                    mensagem=f'Parabéns! Você atingiu o cume da {request.user.profile.montanha_atual.name}!'
                )
            else:
                messages.success(request, 'Material enviado com sucesso!')
            
            return redirect('perfil')
    
    return render(request, 'materials/upload.html', {'form': form})


def buscar_materiais(request):
    """Busca e listagem de materiais com filtros"""
    form = BuscaForm(request.GET)
    materiais = Material.objects.select_related('autor').annotate(
        media_avaliacoes=Avg('avaliacao__nota'),
        total_avaliacoes=Count('avaliacao')
    ).order_by('-data_upload')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        tipo = form.cleaned_data.get('tipo')
        serie = form.cleaned_data.get('serie')
        materia = form.cleaned_data.get('materia')
        
        if query:
            materiais = materiais.filter(
                Q(titulo__icontains=query) | 
                Q(descricao__icontains=query) |
                Q(materia__icontains=query)
            )
        
        if tipo:
            materiais = materiais.filter(tipo=tipo)
        
        if serie:
            materiais = materiais.filter(serie=serie)
            
        if materia:
            materiais = materiais.filter(materia__icontains=materia)
    
    # Paginação
    paginator = Paginator(materiais, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'materiais': page_obj,
    }
    return render(request, 'materials/search.html', context)


def detalhe_material(request, material_id):
    """Detalhes do material com comentários e avaliações"""
    material = get_object_or_404(Material, id=material_id)
    comentarios = Comentario.objects.filter(material=material).select_related('autor').order_by('-data_criacao')
    
    # Verificar se usuário já avaliou
    avaliacao_usuario = None
    if request.user.is_authenticated:
        try:
            avaliacao_usuario = Avaliacao.objects.get(material=material, avaliador=request.user)
        except Avaliacao.DoesNotExist:
            pass
    
    # Formulários
    comentario_form = ComentarioForm()
    avaliacao_form = AvaliacaoForm()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Faça login para interagir com os materiais.')
            return redirect('login')
        
        if 'comentario_submit' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.material = material
                comentario.autor = request.user
                comentario.save()
                
                # Adicionar pontos (+10m por comentário)
                request.user.profile.add_altitude(10)
                
                # Notificar autor do material
                if material.autor != request.user:
                    Notificacao.objects.create(
                        usuario=material.autor,
                        tipo='comentario',
                        titulo='Novo comentário no seu material',
                        mensagem=f'{request.user.get_full_name()} comentou em "{material.titulo}"'
                    )
                
                messages.success(request, 'Comentário adicionado!')
                return redirect('detalhe_material', material_id=material.id)
        
        elif 'avaliacao_submit' in request.POST:
            avaliacao_form = AvaliacaoForm(request.POST)
            if avaliacao_form.is_valid():
                avaliacao, created = Avaliacao.objects.get_or_create(
                    material=material,
                    avaliador=request.user,
                    defaults={'nota': avaliacao_form.cleaned_data['nota']}
                )
                
                if not created:
                    avaliacao.nota = avaliacao_form.cleaned_data['nota']
                    avaliacao.save()
                
                # Adicionar pontos ao autor do material (+5m por avaliação recebida)
                if material.autor != request.user:
                    material.autor.profile.add_altitude(5)
                    
                    # Notificar autor
                    Notificacao.objects.create(
                        usuario=material.autor,
                        tipo='avaliacao',
                        titulo='Nova avaliação no seu material',
                        mensagem=f'{request.user.get_full_name()} avaliou "{material.titulo}" com {avaliacao.nota} estrelas'
                    )
                
                messages.success(request, 'Avaliação registrada!')
                return redirect('detalhe_material', material_id=material.id)
    
    context = {
        'material': material,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'avaliacao_form': avaliacao_form,
        'avaliacao_usuario': avaliacao_usuario,
    }
    return render(request, 'materials/detalhe.html', context)


@login_required
def download_material(request, material_id):
    """Download de arquivo com contagem"""
    material = get_object_or_404(Material, id=material_id)
    
    # Incrementar contador de downloads
    material.downloads += 1
    material.save()
    
    try:
        response = HttpResponse(material.arquivo.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{material.arquivo.name}"'
        return response
    except Exception:
        raise Http404("Arquivo não encontrado")


@login_required
def marcar_notificacao_lida(request, notificacao_id):
    """Marcar notificação como lida"""
    notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
    notificacao.lida = True
    notificacao.save()
    return redirect('perfil')


def ranking_usuarios(request):
    """Ranking de usuários por altitude"""
    usuarios = UserProfile.objects.select_related('user', 'montanha_atual').order_by('-altitude_total')[:20]
    
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'materials/ranking.html', context)


def logout_view(request):
    """Logout personalizado"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('index')