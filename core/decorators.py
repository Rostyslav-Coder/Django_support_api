"""This is decorators module"""

import json
from typing import Callable

from django.http import HttpResponse


def base_error_handler(func: Callable):
    """Handler decorator"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            message = {"error": str(error)}
            status_code = 400
        except TypeError as error:
            message = {"error": str(error)}
            status_code = 500

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(message),
            status=status_code,
        )

    return inner
