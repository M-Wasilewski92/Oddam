import pytest
from users.forms import (
    ContactForm,
    CustomLoginForm,
    CustomUserCreationForm,
    FirstNameChangeForm,
    LastNameChangeForm,
)


@pytest.mark.django_db
def test_custom_user_creation_form():
    form = CustomUserCreationForm(
        data={
            "first_name": "TestUser",
            "last_name": "Testow",
            "email": "test@test.pl",
            "password1": "SilneHasło!2",
            "password2": "SilneHasło!2",
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_custom_login_form(example_user):
    form = CustomLoginForm(data={"username": "test@test.pl", "password": "Test!test"})
    assert form.is_valid()


def test_first_name_change_form():
    form = FirstNameChangeForm(data={"first_name": "Imię testowe"})
    assert form.is_valid()


def test_last_name_change_form():
    form = LastNameChangeForm(data={"last_name": "Nazwisko Testowe"})
    assert form.is_valid()


def test_contact_form():
    form = ContactForm(
        data={
            "first_name": "Test",
            "last_name": "Testow",
            "message": "Testuję wysyłanie Emaila",
        }
    )
    assert form.is_valid()
