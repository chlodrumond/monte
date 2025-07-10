from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponse, Http404
from django.conf import settings
import os

from .models import Material, Avaliacao, Comentario, UserProfile
from .forms import CustomUserCreationForm, MaterialForm, AvaliacaoForm, ComentarioForm, BuscaForm, UserProfileForm

def index(request):
    """Homepage"""
    return render(request, 'core/index.html')

def signup(request):
    """Página de cadastro"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo ao Monte!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    """Página de perfil do usuário"""
    user_materials = Material.objects.filter(user=request.user).order_by('-created_at')
    user_comments = Comentario.objects.filter(user=request.user).order_by('-created_at')[:5]
    user_ratings = Avaliacao.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'user_materials': user_materials,
        'user_comments': user_comments,
        'user_ratings': user_ratings,
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    """Editar perfil do usuário"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def upload_material(request):
    """Upload de materiais"""
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.save()
            messages.success(request, 'Material enviado com sucesso! Você ganhou 50 pontos de altitude!')
            return redirect('profile')
    else:
        form = MaterialForm()
    return render(request, 'core/upload.html', {'form': form})

def search(request):
    """Busca e listagem de materiais"""
    form = BuscaForm(request.GET or None)
    materials = Material.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        tipo = form.cleaned_data.get('tipo')
        materia = form.cleaned_data.get('materia')
        
        if query:
            materials = materials.filter(
                Q(titulo__icontains=query) | 
                Q(descricao__icontains=query) |
                Q(materia__icontains=query)
            )
        
        if tipo:
            materials = materials.filter(tipo=tipo)
        
        if materia:
            materials = materials.filter(materia__icontains=materia)
    
    # Adicionar média de avaliações
    for material in materials:
        avg_rating = material.avaliacoes.aggregate(avg=Avg('nota'))['avg']
        material.avg_rating = avg_rating if avg_rating else 0
        material.total_ratings = material.avaliacoes.count()
    
    # Paginação
    paginator = Paginator(materials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'materials': page_obj.object_list,
    }
    return render(request, 'core/search.html', context)

def material_detail(request, material_id):
    """Detalhes do material"""
    material = get_object_or_404(Material, id=material_id)
    
    # Calcular média das avaliações
    avg_rating = material.avaliacoes.aggregate(avg=Avg('nota'))['avg']
    material.avg_rating = avg_rating if avg_rating else 0
    material.total_ratings = material.avaliacoes.count()
    
    # Verificar se o usuário já avaliou
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Avaliacao.objects.get(material=material, user=request.user)
        except Avaliacao.DoesNotExist:
            pass
    
    # Formulários
    avaliacao_form = AvaliacaoForm()
    comentario_form = ComentarioForm()
    
    # Processar formulários
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para avaliar ou comentar.')
            return redirect('login')
        
        if 'avaliacao_submit' in request.POST:
            avaliacao_form = AvaliacaoForm(request.POST)
            if avaliacao_form.is_valid():
                if user_rating:
                    # Atualizar avaliação existente
                    user_rating.nota = avaliacao_form.cleaned_data['nota']
                    user_rating.comentario = avaliacao_form.cleaned_data['comentario']
                    user_rating.save()
                    messages.success(request, 'Avaliação atualizada com sucesso!')
                else:
                    # Criar nova avaliação
                    avaliacao = avaliacao_form.save(commit=False)
                    avaliacao.material = material
                    avaliacao.user = request.user
                    avaliacao.save()
                    messages.success(request, 'Avaliação enviada com sucesso!')
                return redirect('material_detail', material_id=material.id)
        
        elif 'comentario_submit' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.material = material
                comentario.user = request.user
                comentario.save()
                messages.success(request, 'Comentário enviado com sucesso! Você ganhou 10 pontos de altitude!')
                return redirect('material_detail', material_id=material.id)
    
    # Preencher formulário de avaliação se o usuário já avaliou
    if user_rating:
        avaliacao_form = AvaliacaoForm(instance=user_rating)
    
    context = {
        'material': material,
        'avaliacao_form': avaliacao_form,
        'comentario_form': comentario_form,
        'user_rating': user_rating,
    }
    return render(request, 'core/material_detail.html', context)

@login_required
def download_material(request, material_id):
    """Download de material"""
    material = get_object_or_404(Material, id=material_id)
    
    # Incrementar contador de downloads
    material.increment_downloads()
    
    # Servir arquivo
    file_path = material.arquivo.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{material.arquivo.name}"'
            return response
    
    raise Http404("Arquivo não encontrado")

def ranking(request):
    """Ranking de usuários por pontos de altitude"""
    top_users = UserProfile.objects.select_related('user').order_by('-altitude_points')[:20]
    
    context = {
        'top_users': top_users,
    }
    return render(request, 'core/ranking.html', context)