"""This is configuration for create Users module."""

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserPublicSerializer


class UserCreateAPIView(CreateAPIView):
    """Class to Create Users."""

    serializer_class = UserCreateSerializer

    def post(self, request):  # pylint: disable=W0221
        """Function to create respons after creating users"""

        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        self.perform_create(create_serializer)

        public_serializer = UserPublicSerializer(create_serializer.instance)
        headers = self.get_success_headers(public_serializer.data)
        return Response(
            public_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
