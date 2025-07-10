from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from crispy_forms.bootstrap import FormActions
from .models import Material, Comentario, Avaliacao, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Formulário personalizado de cadastro com validação de email PUC-Rio"""
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email @puc-rio.br'})
    )
    curso = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Curso'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'curso')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Field('username', css_class='form-group mb-3', placeholder='Nome de usuário'),
            Field('email', css_class='form-group mb-3'),
            Field('curso', css_class='form-group mb-3'),
            Field('password1', css_class='form-group mb-3', placeholder='Senha'),
            Field('password2', css_class='form-group mb-3', placeholder='Confirme a senha'),
            FormActions(
                Submit('submit', 'Cadastrar', css_class='btn-acessar w-100')
            )
        )
        
        # Personalizar placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme a senha'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@puc-rio.br'):
            raise ValidationError('Email deve ser do domínio @puc-rio.br')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar o perfil com o curso
            user.profile.curso = self.cleaned_data['curso']
            user.profile.save()
        return user


class CustomLoginForm(forms.Form):
    """Formulário personalizado de login com validação de email PUC-Rio"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', css_class='form-group mb-3'),
            Field('password', css_class='form-group mb-3'),
            FormActions(
                Submit('submit', 'Acessar', css_class='btn-acessar w-100')
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@puc-rio.br'):
            raise ValidationError('Email deve ser do domínio @puc-rio.br')
        return email


class MaterialForm(forms.ModelForm):
    """Formulário para upload de materiais"""
    
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'tipo', 'materia', 'serie', 'arquivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título do material'}),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descreva o material (conteúdo, qual prova, etc.)',
                'rows': 4
            }),
            'materia': forms.TextInput(attrs={'placeholder': 'Nome da matéria'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('titulo', css_class='form-group mb-3'),
            Field('descricao', css_class='form-group mb-3'),
            Row(
                Column('tipo', css_class='form-group col-md-6 mb-3'),
                Column('serie', css_class='form-group col-md-6 mb-3'),
            ),
            Field('materia', css_class='form-group mb-3'),
            Field('arquivo', css_class='form-group mb-3'),
            FormActions(
                Submit('submit', 'Enviar Material', css_class='btn-acessar w-100')
            )
        )


class ComentarioForm(forms.ModelForm):
    """Formulário para comentários"""
    
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'placeholder': 'Deixe seu comentário...',
                'rows': 3,
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('texto', css_class='form-group mb-3'),
            FormActions(
                Submit('submit', 'Comentar', css_class='btn btn-outline-primary')
            )
        )


class AvaliacaoForm(forms.ModelForm):
    """Formulário para avaliações (estrelas)"""
    
    class Meta:
        model = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.Select(choices=[(i, f'{i} ★') for i in range(1, 6)])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nota', css_class='form-group mb-3'),
            FormActions(
                Submit('submit', 'Avaliar', css_class='btn btn-warning')
            )
        )


class BuscaForm(forms.Form):
    """Formulário de busca de materiais"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar materiais...',
            'class': 'form-control'
        })
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + Material.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    serie = forms.ChoiceField(
        choices=[('', 'Todos os períodos')] + Material.SERIE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    materia = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Filtrar por matéria',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='form-group col-md-6 mb-3'),
                Column('materia', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('tipo', css_class='form-group col-md-6 mb-3'),
                Column('serie', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', 'Buscar', css_class='btn btn-primary')
            )
        )