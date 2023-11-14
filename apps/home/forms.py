from django import forms
from apps.gen.models import Gen_Puntaje
from datetime import date
from django.contrib.auth.models import User
class PuntajeForm(forms.ModelForm):
    pun_nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apellido",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_institucion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Institución",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_curso = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Curso",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_materia = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Materia",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_emailprofesor = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico profesor",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    pun_fecha = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(
            attrs={
                "class": "form-control text-secondary",
                "style": "font-family:cursive ; font-size:15px"
            }
        )
    )

    class Meta:
        model = Gen_Puntaje
        fields = (
            'pun_nombre', 'pun_apellido', 'pun_institucion',
            'pun_curso', 'pun_materia', 'pun_email','pun_fecha','pun_emailprofesor'
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name',
                  'username', 'curso', 'institucion']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('El correo electrónico ya está en uso.')
        return email



class ContactForm(forms.Form):
    nombre_apellido = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre y Apellido",
            "style": "font-family: cursive; font-size: 15px"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "style": "font-family: cursive; font-size: 15px"
        })
    )
    asunto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Asunto",
            "style": "font-family: cursive; font-size: 15px"
        })
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Escribe tu mensaje aquí",
            "style": "font-family: cursive; font-size: 15px",
            "rows": 4,  # Ajusta el número de filas según tus preferencias
            "cols": 40  # Ajusta el número de columnas según tus preferencias
        })
    )