import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user(example_user):
    User = get_user_model()
    users = User.objects.all()
    assert len(users) == 1
    assert users[0].email == "test@test.pl"
