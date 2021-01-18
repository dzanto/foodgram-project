from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, password_validation
from django import forms


User = get_user_model()


class CreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")
        labels = {
            'first_name': 'Имя',
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты',
        }
