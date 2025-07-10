from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Material, Avaliacao, Comentario, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    curso = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@puc-rio.br'):
            raise ValidationError("O email deve ser do domínio @puc-rio.br")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar perfil do usuário
            UserProfile.objects.create(
                user=user,
                curso=self.cleaned_data['curso']
            )
        return user

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'tipo', 'materia', 'nivel_serie', 'arquivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do material'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do material'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cálculo I, Física, etc.'}),
            'nivel_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1º período, 2º ano'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            # Verificar tamanho do arquivo (máximo 10MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise ValidationError("O arquivo deve ter no máximo 10MB.")
        return arquivo

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deixe um comentário sobre o material...'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deixe seu comentário...'}),
        }

class BuscaForm(forms.Form):
    query = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar materiais...'})
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + Material.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    materia = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filtrar por matéria...'})
    )
    
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['curso']
        widgets = {
            'curso': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@puc-rio.br'):
            raise ValidationError("O email deve ser do domínio @puc-rio.br")
        return email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Atualizar dados do usuário
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile