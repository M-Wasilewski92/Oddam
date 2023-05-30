from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Imię",
        min_length=3,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-group", "placeholder": "Imię"}),
    )
    last_name = forms.CharField(
        label="Nazwisko",
        min_length=3,
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-group", "placeholder": "Nazwisko"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-group", "placeholder": "Email"}),
        required=True,
    )
    password1 = forms.CharField(
        label="Hasło",
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-group",
                "placeholder": "Hasło",
            }
        ),
    )

    password2 = forms.CharField(
        label="Powtórz hasło",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-group",
                "placeholder": "Powtórz hasło",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Email"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "placeholder": "Hasło"}
        ),
    )


class FirstNameChangeForm(forms.Form):
    first_name = forms.CharField(
        label="Imię",
        min_length=3,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-group", "placeholder": "Imię"}),
    )


class LastNameChangeForm(forms.Form):
    last_name = forms.CharField(
        label="Nazwisko",
        min_length=3,
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-group", "placeholder": "Nazwisko"}
        ),
    )


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Imię"})
    )
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Nazwisko"})
    )
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
