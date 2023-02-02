import pytest
from django.core import mail
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

"""Landing Page Tests"""


@pytest.mark.django_db
def test_landing_page_get(client, example_institution):
    url = reverse('projectapp:landingpage')
    response = client.get(url)
    assert response.status_code == 200
    assert '<h3>Wybierz rzeczy</h3>' in response.content.decode('UTF-8')
    assert '<h2>Komu pomagamy?</h2>' in response.content.decode('UTF-8')
    assert '<div class="title">Fundacja: "Fundacja testowa Pomagam"</div>' in response.content.decode('UTF-8')
    assert '<div class="subtitle">Cel i misja: Opis Testowy Fundacji</div>' in response.content.decode('UTF-8')
    assertTemplateUsed(response, './index.html')
    assertTemplateUsed(response, 'base.html')
    assertTemplateUsed(response, 'partials/_login-register.html')
    assertTemplateUsed(response, 'partials/_footer.html')


# Testing Email Sending
@pytest.mark.django_db
def test_landing_page_mail_post(client, mailoutbox, example_super_user):
    url = reverse('projectapp:landingpage')
    data = {'first_name': 'Test', 'last_name': 'Testow', 'message': 'Testuję wysyłanie Emaila'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'Kontakt'
    assert mail.outbox[0].body == 'Test\nTestow\nTestuję wysyłanie Emaila'


@pytest.mark.django_db
def test_landing_page_post(client, mailoutbox, example_super_user):
    url = reverse('projectapp:landingpage')
    response = client.post(url)
    assert response.status_code == 302
    assert len(mailoutbox) == 0


"""Add Donation test"""


@pytest.mark.django_db
def test_add_donation_logged_in_get(client, example_user):
    url = reverse('projectapp:add')
    client.force_login(example_user)
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, './form.html')
    assertTemplateUsed(response, 'base.html')
    assertTemplateUsed(response, 'partials/_login-register.html')
    assertTemplateUsed(response, 'partials/_footer.html')
    assertTemplateUsed(response, 'partials/_')


@pytest.mark.django_db
def test_add_donation_no_logged_in_get(client):
    url = reverse('projectapp:add')
    response = client.get(url)
    assert response.status_code == 302
