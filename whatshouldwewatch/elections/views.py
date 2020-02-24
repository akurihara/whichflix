from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from whatshouldwewatch.elections import builders
from whatshouldwewatch.elections import manager
from whatshouldwewatch.elections.models import Election
from whatshouldwewatch.users import manager as users_manager


class ElectionsView(APIView):
    def post(self, request: HttpRequest):
        election_description = request.data.get("election_description")
        initiator_name = request.data.get("initiator_name")

        if not election_description:
            return Response(
                {"error": "Missing parameter: `election_description`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not initiator_name:
            return Response(
                {"error": "Missing parameter: `initiator_name`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_token = request.headers["X-Device-ID"]
        device = users_manager.get_or_create_device(device_token)

        election = manager.initiate_election(
            device, initiator_name, election_description
        )

        return Response({"id": election.external_id}, status=status.HTTP_200_OK)


class ElectionDetailView(APIView):
    def get(self, request: HttpRequest, election_id: str):
        election = Election.objects.get(external_id=election_id)
        election_document = builders.build_election_document(election)

        return Response(election_document, status=status.HTTP_200_OK)
