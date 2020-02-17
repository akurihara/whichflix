from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from whatshouldwewatch.elections import manager
from whatshouldwewatch.users import manager as users_manager


class ElectionsView(APIView):
    def get(self, request: HttpRequest, election_id: str):

        return Response({"foo": "bar"}, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        description = request.data.get("description")

        if not description:
            return Response(
                {"error": "Missing parameter: `description`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_token = request.headers["X-Device-ID"]
        device = users_manager.get_or_create_device(device_token)

        election = manager.create_election_for_device(description, device)

        return Response({"id": election.external_id}, status=status.HTTP_200_OK)
