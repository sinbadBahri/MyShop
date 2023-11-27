import pytest

from apps.user.forms import UserCreationForm


# without reCaptcha
@pytest.mark.parametrize(
    "email, first_name, last_name, password1, password2, validity",
    [
        # ("t@test.com", "babak", "zanjani", "eAmYn9Djnd24", "eAmYn9Djnd24", True),
        ("t@test.com", "babak", "zanjani", "eAmYn9Djnd24", "", False),  # no second password
        ("t@test.com", "babak", "zanjani", "eAmYn9Djnd24", "eAmYn9Djnd23", False),  # passwords mismatch
        ("t@.com", "babak", "zanjani", "eAmYn9Djnd24", "eAmYn9Djnd24", False),  # invalid email
        ("t@test.com", "", "zanjani", "eAmYn9Djnd24", "eAmYn9Djnd24", False),  # no first name
    ],
)
@pytest.mark.django_db
def test_user_creation_form(
    client, email, first_name, last_name, password1, password2, validity
):
    form = UserCreationForm(
        data={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password1': password1,
            'password2': password2,
        }
    )
    assert form.is_valid() is validity
