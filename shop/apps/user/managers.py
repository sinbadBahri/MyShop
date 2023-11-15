from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class MyUserManager(BaseUserManager):
    """
    A custom manager for the User model instead of Django UserManager.
    """
    use_in_migrations = True

    def create_user(
            self,
            email,
            first_name,
            last_name,
            is_staff=False,
            is_superuser=False,
            password=None,
            **extra_fields
    ):
        """
        Creates and saves a User with the given email, first name,
        last name and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        if not first_name:
            raise ValueError("User must have a date of birth")

        if not last_name:
            raise ValueError("User must have a last name")

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
        )

        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
        )

        user.save(using=self._db)
        return user
