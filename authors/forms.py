from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, new_attr_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {new_attr_val}'.strip()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Digite seu usuário')
        add_attr(self.fields['email'], 'placeholder', 'Seu e-mail')

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha'
        })

    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha'
        })

    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
    invalid = ['"', "'", '!', '>', '<', ';', ',']

    def clean_password(self):
        data = self.cleaned_data.get('password')
        for string in self.invalid:
            if string in data:
                raise ValidationError(
                    'Não se pode usar caracteres especiais na senha',
                    code='invalid'
                )
        return data

    def clean_password2(self):
        data = self.cleaned_data.get('password2')
        for string in self.invalid:
            if string in data:
                raise ValidationError(
                    'Não se pode usar caracteres especiais na senha',
                    code='invalid'
                )
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'Esse e-mail já está sendo usado',
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    'As senhas devem ser iguais',
                    code='invalid'
                ),
                'password2': ValidationError(
                    'As senhas devem ser iguais',
                    code='invalid'
                )
            })

# Login Form


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
