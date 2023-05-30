import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from projectapp.forms import (
    ContactForm,
    CustomLoginForm,
    CustomUserCreationForm,
    FirstNameChangeForm,
    LastNameChangeForm,
)
from pytest_django.asserts import assertTemplateUsed
from users.tokens import account_activation_token

"""Log in tests"""


def test_login_get(client):
    url = reverse("projectapp:login")
    response = client.get(url)
    form_in_view = response.context["login_form"]
    contact_form_in_view = response.context["contact_form"]
    assert response.status_code == 200
    assert isinstance(form_in_view, CustomLoginForm)
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./login.html")
    assertTemplateUsed(response, "partials/_header.html")
    assert "<h2>Zaloguj się</h2>" in response.content.decode("UTF-8")


# Testing Email Sending
@pytest.mark.django_db
def test_add_donation_mail_post_valid_contact(
    client, mailoutbox, example_super_user, test_email_form
):
    url = reverse("projectapp:login")
    response = client.post(url, test_email_form)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Kontakt"
    assert mail.outbox[0].body == "Test\nTestow\nTestuję wysyłanie Emaila"
    assert response.url.startswith(reverse("projectapp:landingpage"))


@pytest.mark.django_db
def test_login_no_user_post(client):
    url = reverse("projectapp:login")
    data = {"username": "test@test.pl", "password": "Test!test"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:register"))


@pytest.mark.django_db
def test_login_wrong_password_post(client, example_user):
    url = reverse("projectapp:login")
    data = {"username": "test@test.pl", "password": "IamWrong"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert not get_user(client).is_authenticated
    assert response.url.startswith(reverse("projectapp:register"))


@pytest.mark.django_db
def test_login_post(client, example_user):
    url = reverse("projectapp:login")
    data = {"username": "test@test.pl", "password": "Test!test"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert get_user(client).is_authenticated
    assert response.url.startswith(reverse("projectapp:landingpage"))


"""Registration Tests """


def test_registration_get(client):
    url = reverse("projectapp:register")
    response = client.get(url)
    form_in_view = response.context["form"]
    contact_form_in_view = response.context["contact_form"]
    assert response.status_code == 200
    assert isinstance(form_in_view, CustomUserCreationForm)
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./register.html")
    assert "<h2>Załóż konto</h2>" in response.content.decode("UTF-8")


# Testing Email Sending
@pytest.mark.django_db
def test_add_donation_mail_post_valid_contact(
    client, mailoutbox, example_super_user, test_email_form
):
    url = reverse("projectapp:register")
    response = client.post(url, test_email_form)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Kontakt"
    assert mail.outbox[0].body == "Test\nTestow\nTestuję wysyłanie Emaila"
    assert response.url.startswith(reverse("projectapp:landingpage"))


def test_registration_post_no_form(client):
    url = reverse("projectapp:register")
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:register"))


@pytest.mark.django_db
def test_registration_post(client, mailoutbox):
    regular_users = User.objects.filter(is_superuser=False)
    assert len(regular_users) == 0
    url = reverse("projectapp:register")
    data = {
        "first_name": "TestUser",
        "last_name": "Testow",
        "email": "test@test.pl",
        "password1": "SilneHasło!2",
        "password2": "SilneHasło!2",
    }
    response = client.post(url, data)
    regular_users = User.objects.filter(is_superuser=False)
    assert response.status_code == 302
    assert len(regular_users) == 1
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Aktywacja Konta"
    assert response.url.startswith(reverse("projectapp:login"))


@pytest.mark.django_db
def test_registration_post_invalid_form(client, mailoutbox):
    regular_users = User.objects.filter(is_superuser=False)
    assert len(regular_users) == 0
    url = reverse("projectapp:register")
    data = {
        "first_name": "TestUser",
        "last_name": "Testow",
        "email": "test@test.pl",
        "password1": "SilneHasło!1",
        "password2": "SilneHasło!15",
    }
    response = client.post(url, data)
    regular_users = User.objects.filter(is_superuser=False)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:register"))
    assert len(regular_users) == 0
    assert len(mailoutbox) == 0


""" User Activation tests """


@pytest.mark.django_db
def test_user_activation_valid(client, inactive_user):
    is_active_users = User.objects.filter(is_active=True)
    assert len(is_active_users) == 0
    assert not inactive_user.is_active
    uid64 = urlsafe_base64_encode(force_bytes(inactive_user.id))
    token = account_activation_token.make_token(inactive_user)
    url = reverse("projectapp:activate", args=[uid64, token])
    response = client.get(url)
    is_active_users = User.objects.filter(is_active=True)
    assert response.status_code == 302
    assert len(is_active_users) == 1
    assert response.url.startswith(reverse("projectapp:login"))


@pytest.mark.django_db
def test_user_activation_not_valid(client, inactive_user):
    uid64 = urlsafe_base64_encode(force_bytes(inactive_user.id))
    url = reverse("projectapp:activate", args=[{uid64}, {15}])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:landingpage"))
    assert not inactive_user.is_active


"""Testing User Settings"""


@pytest.mark.django_db
def test_user_settings_get(client, example_user):
    url = reverse("projectapp:settings")
    client.force_login(example_user)
    response = client.get(url)
    contact_form_in_view = response.context["contact_form"]
    first_name_form_in_view = response.context["first_name_form"]
    last_name_form_in_view = response.context["last_name_form"]
    assert response.status_code == 200
    assert isinstance(first_name_form_in_view, FirstNameChangeForm)
    assert isinstance(last_name_form_in_view, LastNameChangeForm)
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./user-settings.html")
    assert f"<h3> Imię: {example_user.first_name}</h3>" in response.content.decode(
        "UTF-8"
    )


@pytest.mark.django_db
def test_user_settings_get_not_logged_in(client):
    url = reverse("projectapp:settings")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:login"))


@pytest.mark.django_db
def test_user_settings_post_change_first_name(client, example_user):
    url = reverse("projectapp:settings")
    client.force_login(example_user)
    data = {"first_name": "Imię testowe", "user_id": example_user.pk}
    response = client.post(url, data)
    assert response.status_code == 200
    assertTemplateUsed(response, "./user-settings.html")


@pytest.mark.django_db
def test_user_settings_post_change_last_name(
    client,
    example_user,
):
    url = reverse("projectapp:settings")
    client.force_login(example_user)
    data = {"last_name": "Nazwisko Testowe", "user_id": example_user.pk}
    response = client.post(url, data)
    assert response.status_code == 200
    assertTemplateUsed(response, "./user-settings.html")


"""Password Reset Tests"""


@pytest.mark.django_db
def test_user_settings_post_change_password(client, example_user, mailoutbox):
    url = reverse("projectapp:password_reset")
    client.force_login(example_user)
    data = {"email": "test@test.pl"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Prośba o Reset hasła"
    assert "Link jednorazowego użytku." in mail.outbox[0].body


@pytest.mark.django_db
def test_user_settings_post_change_password_invalid_email(
    client, example_user, mailoutbox
):
    url = reverse("projectapp:password_reset")
    client.force_login(example_user)
    data = {"email": "wrong@test.pl"}
    response = client.post(url, data)
    assert response.status_code == 200
    assertTemplateUsed(response, "password_reset_no_user.html")
