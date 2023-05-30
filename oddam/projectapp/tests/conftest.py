import pytest
from projectapp.models import Category, Donation, Institution


@pytest.fixture()
def example_category():
    category = Category.objects.create(name="Koce")
    return category


@pytest.fixture()
def example_institution(example_category):
    institution = Institution.objects.create(
        name="Fundacja testowa Pomagam",
        description="Opis Testowy Fundacji",
        type="Fundacja",
    )
    institution.categories.add(example_category)
    return institution


@pytest.fixture()
def example_donation(example_user, example_institution):
    donation = Donation.objects.create(
        quantity=5,
        institution=example_institution,
        address="Test adres",
        phone_number="123123123",
        city="Testowo",
        zip_code="12-345",
        pick_up_date="2023-02-02",
        pick_up_time="11:30",
        pick_up_comment="Testowy Komentarz",
        user=example_user,
    )
    return donation
