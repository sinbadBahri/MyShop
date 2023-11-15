from datetime import timezone

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db.models import CharField

from .managers import MyUserManager


class User(AbstractBaseUser):
    """
    The User class is a custom implementation of the Django AbstractBaseUser model.
    It represents a user in the system and provides functionalities for user authentication and authorization.
    """

    full_name_validator = RegexValidator(
        regex=r"^[a-zA-Z]+$",
        message="Only letters are allowed.",
        code='invalid',
    )

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        help_text="Required. Must be a valid email address like example@example.com",
        error_messages={
            "unique": "A user with the same email already exists.",
            "max_length": "You email's length can not be more than 255 characters",
        },
    )
    first_name = models.CharField(
        max_length=32,
        help_text="Enter your first name",
        validators=[full_name_validator],
        error_messages={
            'max_length': "First Name's length is lower than 32",
        },
    )
    last_name = models.CharField(
        max_length=32,
        help_text="Enter your family name",
        validators=[full_name_validator],
        error_messages={
            'max_length': "Last Name's length is lower than 32",
        },
    )
    # date_of_birth = models.DateField()
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

    def __str__(self) -> CharField:
        return self.email
