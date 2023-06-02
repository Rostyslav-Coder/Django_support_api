"""This is module to create Data Base Table with fields."""
from django.db import models


class Users(models.Model):
    """Class to create Users Table"""
    username = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField()

    class Meta:
        """Meta class to rename users table"""
        db_table = "users"
