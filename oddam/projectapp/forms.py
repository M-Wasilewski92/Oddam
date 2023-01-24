from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Imię', min_length=3, max_length=150,
                                 widget=forms.TextInput(attrs=
                                                        {'class': 'form-group',
                                                         'placeholder': 'Imię'}))
    last_name = forms.CharField(label='Nazwisko', min_length=3, max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-group',
                                                              'placeholder': 'Nazwisko'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-group',
                                                            'placeholder': 'Email'}), required=True)
    password1 = forms.CharField(label='Hasło', strip=False, widget=forms.PasswordInput(attrs=
                                                                                       {"autocomplete": "new-password",
                                                                                        'class': 'form-group',
                                                                                        'placeholder': 'Hasło'}))

    password2 = forms.CharField(label='Powtórz hasło', strip=False,
                                widget=forms.PasswordInput(attrs=
                                                           {"autocomplete": "new-password",
                                                            'class': 'form-group',
                                                            'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'Email'}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'placeholder': 'Hasło'}),
    )


class DonationCreationForm(forms.Form):
    quantity = forms.IntegerField()
    address = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=30)
    zip_code = forms.CharField(max_length=10)
    pick_up_date = forms.DateField(widget=forms.DateInput)
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(widget=forms.Textarea)
    institution_id = forms.IntegerField()
    category_ids = forms.CharField(max_length=5)
