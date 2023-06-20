"""This is module to save hashed data"""
from enum import IntEnum


class Role(IntEnum):
    """This is class to create users role"""

    ADMIN = 1
    MANAGER = 2
    USER = 3
