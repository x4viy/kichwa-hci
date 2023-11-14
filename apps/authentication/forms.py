# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError
from apps.sis.models import Sis_Rol
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control",
                "style": "font-family:cursive ; font-size:15px"

            }
        ),
        # required=False  # La contraseña no será obligatoria
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apellido",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo Electrónico",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar Contraseña",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        ))
    accept_terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'Debes aceptar los términos y condiciones.',
        },
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'form-control'}))

    rol = forms.ModelChoiceField(
        queryset=Sis_Rol.objects.exclude(rol_id=1),
        widget=forms.Select(attrs={"class": " bg-white form-select text-secondary", "style": "font-family:cursive ; font-size:15px"}),
        label="Rol"
    )
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2',
                  'rol')


