from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, F
from django.db.models.functions import Coalesce, Cast
from django.db import models
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from .models import (
    Material, Comentario, Avaliacao, UserProfile, 
    MountainLevel, Notificacao, MountainAchievement,
    SocialShare, MaterialFavorito
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
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            # Try to find user by username or email
            user = None
            if '@' in username_or_email:
                # It's an email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    messages.error(request, 'Email não encontrado.')
            else:
                # It's a username
                user = authenticate(request, username=username_or_email, password=password)
                if user is None:
                    messages.error(request, 'Usuário ou senha incorretos.')
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Bem-vindo de volta, {user.get_full_name()}!')
                    return redirect('perfil')
                else:
                    messages.error(request, 'Conta não ativada. Verifique seu email para ativar a conta.')
            elif '@' not in username_or_email:
                messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    """Cadastro de usuários com validação de email PUC-Rio e confirmação por email"""
    if request.user.is_authenticated:
        return redirect('perfil')
    
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Criar usuário mas deixar inativo até confirmação
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Criar perfil manualmente já que o usuário está inativo
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.curso = form.cleaned_data['curso']
            profile.save()
            
            # Enviar email de confirmação
            send_confirmation_email(request, user)
            
            username = form.cleaned_data.get('username')
            messages.success(
                request, 
                f'Conta criada para {username}! Verifique seu email PUC-Rio para confirmar a conta.'
            )
            return redirect('login')
    
    return render(request, 'registration/signup.html', {'form': form})


def send_confirmation_email(request, user):
    """Envia email de confirmação para o usuário"""
    current_site = get_current_site(request)
    mail_subject = 'Ative sua conta Monte Platform'
    
    # Gerar token de ativação
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # URL de ativação
    activation_link = f"http://{current_site.domain}/ativar/{uid}/{token}/"
    
    message = f"""
    Olá {user.get_full_name()},
    
    Bem-vindo à Monte Platform!
    
    Para ativar sua conta, clique no link abaixo:
    {activation_link}
    
    Este link expira em 24 horas.
    
    Se você não criou esta conta, ignore este email.
    
    Equipe Monte Platform
    """
    
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def activate_account(request, uidb64, token):
    """Ativa a conta do usuário através do link no email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Conta ativada com sucesso! Você já pode fazer login.')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido ou expirado.')
        return redirect('signup')


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


@login_required
def buscar_materiais(request):
    """Busca e listagem de materiais com filtros - LOGIN REQUERIDO"""
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
            materiais = materiais.filter(grau=serie)
            
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


@login_required
def favoritar_material(request, material_id):
    """Adicionar/remover material dos favoritos"""
    material = get_object_or_404(Material, id=material_id)
    favorito, created = MaterialFavorito.objects.get_or_create(
        usuario=request.user,
        material=material
    )
    
    if not created:
        favorito.delete()
        messages.success(request, 'Material removido dos favoritos.')
    else:
        messages.success(request, 'Material adicionado aos favoritos!')
    
    return redirect('detalhe_material', material_id=material_id)


@login_required
def meus_favoritos(request):
    """Lista de materiais favoritos do usuário"""
    favoritos = MaterialFavorito.objects.filter(usuario=request.user).select_related('material', 'material__autor')
    
    paginator = Paginator(favoritos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'favoritos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'materials/favoritos.html', context)


def compartilhar_material(request, material_id, plataforma):
    """Registrar compartilhamento social e redirecionar"""
    material = get_object_or_404(Material, id=material_id)
    
    # Registrar o compartilhamento
    SocialShare.objects.create(
        material=material,
        usuario=request.user if request.user.is_authenticated else None,
        plataforma=plataforma
    )
    
    # URLs para compartilhamento
    material_url = request.build_absolute_uri(
        f"/materiais/{material_id}/"
    )
    texto = f"Confira este material: {material.titulo}"
    
    urls = {
        'whatsapp': f"https://wa.me/?text={texto} - {material_url}",
        'twitter': f"https://twitter.com/intent/tweet?text={texto}&url={material_url}",
        'facebook': f"https://www.facebook.com/sharer/sharer.php?u={material_url}",
        'email': f"mailto:?subject={material.titulo}&body={texto} - {material_url}",
    }
    
    if plataforma in urls:
        return redirect(urls[plataforma])
    
    return redirect('detalhe_material', material_id=material_id)


@login_required
def materiais_populares(request):
    """Lista de materiais mais populares baseada em algoritmo de curadoria - LOGIN REQUERIDO"""
    # Materiais ordenados por popularidade (visualizações, downloads, avaliações)
    materiais = Material.objects.annotate(
        media_avaliacoes=Coalesce(Avg('avaliacao__nota'), 0.0, output_field=models.FloatField()),
        total_avaliacoes=Count('avaliacao'),
        popularidade_score=(
            Cast(F('visualizacoes'), models.FloatField()) * 0.1 + 
            Cast(F('downloads'), models.FloatField()) * 0.5 + 
            F('media_avaliacoes') * 2.0 +
            Cast(F('total_avaliacoes'), models.FloatField()) * 0.3
        )
    ).order_by('-popularidade_score', '-data_upload')
    
    # Filtros opcionais
    tipo = request.GET.get('tipo')
    serie = request.GET.get('serie')
    
    if tipo:
        materiais = materiais.filter(tipo=tipo)
    if serie:
        materiais = materiais.filter(grau=serie)
    
    paginator = Paginator(materiais, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'materiais': page_obj,
        'page_obj': page_obj,
        'titulo': 'Materiais Populares',
        'tipo_atual': tipo,
        'serie_atual': serie,
        'tipos': Material.TIPO_CHOICES,
        'series': Material.GRAU_CHOICES,
    }
    return render(request, 'materials/populares.html', context)


@login_required
def materiais_destaque(request):
    """Materiais em destaque selecionados pela curadoria - LOGIN REQUERIDO"""
    materiais = Material.objects.filter(destaque=True).select_related('autor').order_by('-data_upload')
    
    paginator = Paginator(materiais, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'materiais': page_obj,
        'page_obj': page_obj,
        'titulo': 'Materiais em Destaque',
    }
    return render(request, 'materials/destaque.html', context)


@login_required
def notificacoes_usuario(request):
    """Lista todas as notificações do usuário"""
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    # Marcar todas como lidas ao visualizar
    notificacoes.filter(lida=False).update(lida=True)
    
    paginator = Paginator(notificacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'notificacoes': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'materials/notificacoes.html', context)


# Helper function to check if user is admin
def is_admin_user(user):
    return user.is_authenticated and user.email == settings.ADMIN_EMAIL

@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """Dashboard administrativo - apenas para email específico"""
    # Estatísticas gerais
    total_usuarios = User.objects.count()
    usuarios_ativos = User.objects.filter(is_active=True).count()
    usuarios_inativos = User.objects.filter(is_active=False).count()
    total_materiais = Material.objects.count()
    
    # Usuários recentes
    usuarios_recentes = User.objects.select_related('profile').order_by('-date_joined')[:10]
    
    # Materiais recentes
    materiais_recentes = Material.objects.select_related('autor').order_by('-data_upload')[:10]
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_ativos': usuarios_ativos,
        'usuarios_inativos': usuarios_inativos,
        'total_materiais': total_materiais,
        'usuarios_recentes': usuarios_recentes,
        'materiais_recentes': materiais_recentes,
    }
    return render(request, 'materials/admin_dashboard.html', context)


@user_passes_test(is_admin_user)
def admin_users(request):
    """Lista de usuários para administração"""
    usuarios = User.objects.select_related('profile').order_by('-date_joined')
    
    # Filtros
    filtro = request.GET.get('filtro')
    if filtro == 'ativos':
        usuarios = usuarios.filter(is_active=True)
    elif filtro == 'inativos':
        usuarios = usuarios.filter(is_active=False)
    
    # Busca
    busca = request.GET.get('busca')
    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) |
            Q(email__icontains=busca) |
            Q(first_name__icontains=busca) |
            Q(last_name__icontains=busca)
        )
    
    paginator = Paginator(usuarios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'usuarios': page_obj,
        'page_obj': page_obj,
        'filtro': filtro,
        'busca': busca,
    }
    return render(request, 'materials/admin_users.html', context)


@user_passes_test(is_admin_user)
def admin_delete_user(request, user_id):
    """Deletar usuário - apenas para admin"""
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Não permitir deletar próprio usuário
        if user_to_delete == request.user:
            messages.error(request, 'Você não pode deletar sua própria conta.')
        else:
            username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request, f'Usuário {username} foi removido com sucesso.')
    
    return redirect('admin_users')


@user_passes_test(is_admin_user)
def admin_materials(request):
    """Lista de materiais para administração"""
    materiais = Material.objects.select_related('autor').order_by('-data_upload')
    
    # Filtros
    tipo = request.GET.get('tipo')
    if tipo:
        materiais = materiais.filter(tipo=tipo)
    
    # Busca
    busca = request.GET.get('busca')
    if busca:
        materiais = materiais.filter(
            Q(titulo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(autor__username__icontains=busca)
        )
    
    paginator = Paginator(materiais, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'materiais': page_obj,
        'page_obj': page_obj,
        'tipo': tipo,
        'busca': busca,
        'tipos': Material.TIPO_CHOICES,
    }
    return render(request, 'materials/admin_materials.html', context)


@user_passes_test(is_admin_user)
def admin_delete_material(request, material_id):
    """Deletar material - apenas para admin"""
    if request.method == 'POST':
        material = get_object_or_404(Material, id=material_id)
        titulo = material.titulo
        
        # Deletar arquivo físico se existir
        if material.arquivo:
            try:
                material.arquivo.delete()
            except:
                pass
        
        material.delete()
        messages.success(request, f'Material "{titulo}" foi removido com sucesso.')
    
    return redirect('admin_materials')