from . models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Форма регистрации


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'example',
    })
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '*******',
    })
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '*******',
    })
    )
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'example@gmail.com',
    })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'img',
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'example',
    })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '*******',
    })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )
