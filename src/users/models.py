"""This is module to create User Data Base Table with fields."""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Class to create Users Table"""

    email = models.EmailField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(default=True)

    role = models.PositiveSmallIntegerField()

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Class Meta to rename message table"""

        db_table = "users"

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.email
