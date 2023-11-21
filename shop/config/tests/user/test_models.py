import pytest

from apps.user.managers import MyUserManager

pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_handle_non_ascii_characters(self, user_factory):
        user = user_factory(first_name="Babak", last_name="Zanjani")
        assert user.get_full_name() == "Babak Zanjani"

    def test_return_first_name_when_exists(self, user_factory):
        user = user_factory(first_name="Shahram", last_name="Jazayeri")
        assert user.get_short_name() == "Shahram"

    def test_return_email_as_string(self, user_factory):
        user = user_factory(email="test@example.com")
        assert user.__str__() == "test@example.com"

    def test_create_user_with_empty_email(self, user_factory):
        user_factory.objects = MyUserManager()
        with pytest.raises(ValueError):
            user_factory.objects.create_user(
                email='',
                first_name='Babak',
                last_name='Zanjani',
                password='password'
            )

    def test_create_user_with_empty_first_name(self, user_factory):
        user_factory.objects = MyUserManager()
        with pytest.raises(ValueError):
            user_factory.objects.create_user(
                email='test@example.com',
                first_name='',
                last_name='Zanjani',
                password='password'
            )

    def test_create_user_with_empty_last_name(self, user_factory):
        user_factory.objects = MyUserManager()
        with pytest.raises(ValueError):
            user_factory.objects.create_user(
                email='test@example.com',
                first_name='Babak',
                last_name='',
                password='password'
            )
