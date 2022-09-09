from django import forms
from django.contrib.auth.models import User


class RegisterForms(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # labels = {
        #     'username': 'Digite seu usuario'
        # }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite aqui',
                # 'class': 'classetal-balbal',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Sua senha vai aqui',
            })
        }
