from django import forms
from django.contrib.auth.models import User
from core.models import Client
from datetime import date


class ClientRegisterForm(forms.Form):
    last_name_client = forms.CharField(max_length=20, label="Фамилия")
    first_name_client = forms.CharField(max_length=20, label="Имя")
    middle_name_client = forms.CharField(max_length=20, label="Отчество")
    phone_number_client = forms.CharField(max_length=12, label="Телефон")
    birth_date = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"}))
    email_client = forms.EmailField(max_length=30, label="Email (логин)")
    password_client = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        label="Пароль"
    )
    password_client2 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        label="Повторите пароль"
    )

    def clean_birth_date(self):
        value = self.cleaned_data["birth_date"]
        if value >= date.today():
            raise forms.ValidationError("Дата рождения должна быть в прошлом.")
        return value

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password_client")
        p2 = cleaned.get("password_client2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned
