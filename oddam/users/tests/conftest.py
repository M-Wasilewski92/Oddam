import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


@pytest.fixture()
def example_user():
    user = User.objects.create_user(
        email="test@test.pl",
        username="test@test.pl",
        first_name="Test",
        last_name="Testow",
        password="Test!test",
    )
    return user


@pytest.fixture()
def inactive_user():
    User = get_user_model()
    user = User.objects.create_user(
        email="testy@test.pl",
        username="testy@test.pl",
        first_name="Test",
        last_name="Testow",
        password="Test!test",
        is_active=False,
    )
    return user


@pytest.fixture()
def example_super_user():
    super_user = User.objects.create_superuser(
        username="aa", email="test@test.pl", password="aa"
    )
    return super_user


@pytest.fixture()
def test_email_form():
    data = {
        "first_name": "Test",
        "last_name": "Testow",
        "message": "Testuję wysyłanie Emaila",
    }
    return data
