from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Thread, Comment

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,  help_text="Введите почту с доменом @edu.hse.ru")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        email = self.cleaned_data.get("email")
        if not email.endswith("@edu.hse.ru"):
            raise forms.ValidationError("Регистрация доступна только с адресами @edu.hse.ru.")

        user = super().save(commit=False)
        user.email = email
        user.is_active = False  # Деактивируем пользователя до подтверждения
        if commit:
            user.save()
        return user