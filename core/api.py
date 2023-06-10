"""API configuration for create Users, Reequests & Messages."""

import json

from django.http import HttpResponse

from core.decorators import base_error_handler
from core.models import User


@base_error_handler
def create_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    # Serialize data into the internal structure
    data: dict = json.loads(request.body)

    # Save user to the database table
    user = User.objects.create_user(**data)

    # Create response representation
    result = {
        "id": user.pk,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
    }

    return HttpResponse(
        content_type="application/json", content=json.dumps(result)
    )
