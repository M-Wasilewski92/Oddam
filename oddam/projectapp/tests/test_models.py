import pytest
import datetime
from django.contrib.auth import get_user_model
from projectapp.models import Category, Institution, Donation


@pytest.mark.django_db
def test_create_user(example_user):
    User = get_user_model()
    users = User.objects.all()
    assert len(users) == 1
    assert users[0].email == 'test@test.pl'


@pytest.mark.django_db
def test_create_category_model(example_category):
    all_categories = Category.objects.all()
    assert len(all_categories) == 1
    assert all_categories[0].name == 'Koce'


@pytest.mark.django_db
def test_create_institution_model(example_category):
    institution = Institution.objects.create(name="Fundacja testowa Pomagam", description="Opis Testowy Fundacji",
                                             type='Fundacja')
    all_institutions = Institution.objects.all()
    assert len(all_institutions) == 1
    assert all_institutions[0].name == 'Fundacja testowa Pomagam'
    assert all_institutions[0].description == 'Opis Testowy Fundacji'
    assert all_institutions[0].type == 'Fundacja'


@pytest.mark.django_db
def test_create_donation(example_institution, example_user):
    donation = Donation.objects.create(quantity=5, institution=example_institution, address='Test adres',
                                       phone_number='123123123', city='Testowo', zip_code='12-345',
                                       pick_up_date='2023-02-02', pick_up_time='11:30',
                                       pick_up_comment="Testowy Komentarz", user=example_user)
    all_donations = Donation.objects.all()
    assert len(all_donations) == 1
    assert all_donations[0].quantity == 5
    assert all_donations[0].institution == example_institution
    assert all_donations[0].address == 'Test adres'
    assert all_donations[0].phone_number == '123123123'
    assert all_donations[0].city == 'Testowo'
    assert all_donations[0].zip_code == '12-345'
    assert all_donations[0].pick_up_date == datetime.date(2023, 2, 2)
    assert all_donations[0].pick_up_time == datetime.time(hour=11, minute=30)
    assert all_donations[0].pick_up_comment == 'Testowy Komentarz'
    assert all_donations[0].user == example_user
