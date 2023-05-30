import pytest
from projectapp.forms import ContactForm, DonationCreationForm, IsTakenForm


@pytest.mark.django_db
def test_donation_form(example_user, example_institution, example_category):
    form = DonationCreationForm(
        data={
            "quantity": 5,
            "address": "Test adres",
            "phone_number": "123123123",
            "city": "Testowo",
            "zip_code": "12-345",
            "pick_up_date": "2023-02-02",
            "pick_up_time": "11:30",
            "pick_up_comment": "Testowy Komentarz",
            "institution_id": 1,
            "category_ids": "1",
        }
    )
    assert form.is_valid()


def test_is_taken_form():
    form = IsTakenForm(data={"is_taken": True})
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
