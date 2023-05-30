import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from projectapp.forms import ContactForm, DonationCreationForm, IsTakenForm
from projectapp.models import Donation
from pytest_django.asserts import assertTemplateUsed

"""Landing Page Tests"""


# connection method GET
@pytest.mark.django_db
def test_landing_page_get(client, example_institution):
    url = reverse("projectapp:landingpage")
    response = client.get(url)
    form_in_view = response.context["contact_form"]
    assert response.status_code == 200
    assert isinstance(form_in_view, ContactForm)
    assert "<h3>Wybierz rzeczy</h3>" in response.content.decode("UTF-8")
    assert "<h2>Komu pomagamy?</h2>" in response.content.decode("UTF-8")
    assert (
        '<div class="title">Fundacja: "Fundacja testowa Pomagam"</div>'
        in response.content.decode("UTF-8")
    )
    assert (
        f'<div class="subtitle">Cel i misja: {example_institution.description}</div>'
        in response.content.decode("UTF-8")
    )
    assertTemplateUsed(response, "./index.html")
    assertTemplateUsed(response, "base.html")
    assertTemplateUsed(response, "partials/_login-register.html")
    assertTemplateUsed(response, "partials/_footer.html")


# connection method POST
# Testing Email Sending
@pytest.mark.django_db
def test_landing_page_mail_post(
    client, mailoutbox, example_super_user, test_email_form
):
    url = reverse("projectapp:landingpage")
    response = client.post(url, test_email_form)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Kontakt"
    assert mail.outbox[0].body == "Test\nTestow\nTestuję wysyłanie Emaila"
    assert response.url.startswith(reverse("projectapp:landingpage"))


@pytest.mark.django_db
def test_landing_page_post(client, mailoutbox, example_super_user):
    url = reverse("projectapp:landingpage")
    response = client.post(url)
    assert response.status_code == 302
    assert len(mailoutbox) == 0
    assert response.url.startswith(reverse("projectapp:landingpage"))


"""Add Donation tests"""


# connection method GET
@pytest.mark.django_db
def test_add_donation_logged_in_get(client, example_user):
    url = reverse("projectapp:add")
    client.force_login(example_user)
    response = client.get(url)
    form_in_view = response.context["form"]
    contact_form_in_view = response.context["contact_form"]
    assert response.status_code == 200
    assert isinstance(form_in_view, DonationCreationForm)
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./form.html")
    assertTemplateUsed(response, "base.html")
    assertTemplateUsed(response, "partials/_login-register.html")
    assertTemplateUsed(response, "partials/_footer.html")
    assert (
        '<div class="slogan--steps-title">Wystarczą 4 proste kroki:</div>'
        in response.content.decode("UTF-8")
    )


@pytest.mark.django_db
def test_add_donation_not_logged_in_get(client):
    url = reverse("projectapp:add")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:landingpage"))


# connection method POST
@pytest.mark.django_db
def test_add_donation_not_logged_in_post(client):
    url = reverse("projectapp:add")
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:landingpage"))


@pytest.mark.django_db
def test_add_donation_post_form_not_valid(client, example_user):
    url = reverse("projectapp:add")
    client.force_login(example_user)
    response = client.get(url)
    assert response.status_code == 200


# Testing Email Sending
@pytest.mark.django_db
def test_add_donation_mail_post_valid_contact(
    client, mailoutbox, example_user, example_super_user, test_email_form
):
    url = reverse("projectapp:add")
    client.force_login(example_user)
    response = client.post(url, test_email_form)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Kontakt"
    assert mail.outbox[0].body == "Test\nTestow\nTestuję wysyłanie Emaila"
    assert response.url.startswith(reverse("projectapp:landingpage"))


@pytest.mark.django_db
def test_add_donation_post_form_valid(
    client, example_user, example_institution, example_category
):
    donations = Donation.objects.all()
    assert len(donations) == 0
    url = reverse("projectapp:add")
    client.force_login(example_user)
    data = {
        "quantity": 5,
        "address": "Test adres",
        "phone_number": "123123123",
        "city": "Testowo",
        "zip_code": "12-345",
        "pick_up_date": "2023-02-02",
        "pick_up_time": "11:30",
        "pick_up_comment": "Testowy Komentarz",
        "institution_id": example_institution.id,
        "category_ids": str(example_category.id),
    }
    response = client.post(url, data)
    donations = Donation.objects.all()
    assert response.status_code == 302
    assert len(donations) == 1
    assert donations[0].quantity == 5
    assert donations[0].pick_up_comment == "Testowy Komentarz"
    assert response.url.startswith(reverse("projectapp:donation"))


""" SuccessDonation tests """


def test_success_donation(client):
    url = reverse("projectapp:donation")
    response = client.get(url)
    contact_form_in_view = response.context["contact_form"]
    assert response.status_code == 200
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./form-confirmation.html")
    assert (
        '<li><a href="#contact" class="btn btn--without-border">Kontakt</a></li>'
        in response.content.decode("UTF-8")
    )


""" User Profile tests """


@pytest.mark.django_db
def test_user_profile_get(client, example_user, example_donation):
    url = reverse("projectapp:profile")
    client.force_login(example_user)
    response = client.get(url)
    contact_form_in_view = response.context["contact_form"]
    form_in_view = response.context["form"]
    assert response.status_code == 200
    assert isinstance(form_in_view, IsTakenForm)
    assert isinstance(contact_form_in_view, ContactForm)
    assertTemplateUsed(response, "./user-page.html")
    assert "<p>Dotacja nie odebrana:</p>" in response.content.decode("UTF-8")


@pytest.mark.django_db
def test_userprofile_get_not_logged_in(client, example_user):
    url = reverse("projectapp:profile")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:landingpage"))


@pytest.mark.django_db()
def test_user_profile_post(client, example_user, example_donation):
    assert not example_donation.is_taken
    assert len(Donation.objects.filter(is_taken=True)) == 0
    url = reverse("projectapp:profile")
    client.force_login(example_user)
    data = {"is_taken": True, "don_id": example_donation.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert len(Donation.objects.filter(is_taken=True)) == 1
    assert response.url.startswith(reverse("projectapp:profile"))


@pytest.mark.django_db
def test_user_profile_post_no_form(client, example_user, example_donation):
    url = reverse("projectapp:profile")
    client.force_login(example_user)
    data = {"don_id": example_donation.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:profile"))


@pytest.mark.django_db
def test_user_profile_post_no_donation_id(client, example_user, example_donation):
    url = reverse("projectapp:profile")
    client.force_login(example_user)
    data = {"is_taken": True}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse("projectapp:profile"))
