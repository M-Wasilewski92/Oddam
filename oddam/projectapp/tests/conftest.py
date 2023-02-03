import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from projectapp.models import Category, Institution, Donation


@pytest.fixture()
def example_user():
    User = get_user_model()
    user = User.objects.create_user(email='test@test.pl', username='test@test.pl',
                                    first_name='Test', last_name='Testow', password='Test!test')
    return user

@pytest.fixture()
def inactive_user():
    User = get_user_model()
    user = User.objects.create_user(email='testy@test.pl', username='testy@test.pl',
                                    first_name='Test', last_name='Testow', password='Test!test', is_active=False)
    return user
@pytest.fixture()
def example_super_user():
    super_user = User.objects.create_superuser(username='aa', email='test@test.pl', password='aa')
    return super_user


@pytest.fixture()
def example_category():
    category = Category.objects.create(name="Koce")
    return category


@pytest.fixture()
def example_institution(example_category):
    institution = Institution.objects.create(name="Fundacja testowa Pomagam", description="Opis Testowy Fundacji",
                                             type='Fundacja')
    institution.categories.add(example_category)
    return institution


@pytest.fixture()
def example_donation(example_user, example_institution):
    donation = Donation.objects.create(quantity=5, institution=example_institution, address='Test adres',
                                       phone_number='123123123', city='Testowo', zip_code='12-345',
                                       pick_up_date='2023-02-02', pick_up_time='11:30',
                                       pick_up_comment="Testowy Komentarz", user=example_user)
    return donation


@pytest.fixture()
def test_email_form():
    data = {'first_name': 'Test', 'last_name': 'Testow', 'message': 'Testuję wysyłanie Emaila'}
    return data

