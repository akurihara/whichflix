from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from whatshouldwewatch.elections import builders
from whatshouldwewatch.elections import manager
from whatshouldwewatch.elections.models import Election
from whatshouldwewatch.users import manager as users_manager

election_document_schema = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(
            type="string",
            description="A unique identifier for the election.",
            example="nygr37",
        ),
        "description": openapi.Schema(
            type="string",
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        ),
    },
)


class CandidatesView(APIView):
    @swagger_auto_schema(
        operation_id="Create Candidate", responses={201: "Null response", 404: ""}
    )
    def post(self, request: HttpRequest, election_id: str):
        pass


class ElectionsView(APIView):
    device_id = openapi.Parameter(
        name="X-Device-ID",
        in_=openapi.IN_HEADER,
        description="Unique identifier for the device.",
        type=openapi.TYPE_STRING,
        required=True,
    )
    request_body = openapi.Schema(
        type="object",
        properties={
            "election_description": openapi.Schema(
                type="string",
                description="Description of the election.",
                example="Movie night in Brooklyn!",
            ),
            "initiator_name": openapi.Schema(
                type="string",
                description="Name of the user initiating the election.",
                example="John",
            ),
        },
        required=["election_description", "initiator_name"],
    )

    @swagger_auto_schema(
        operation_id="Create Election",
        manual_parameters=[device_id],
        request_body=request_body,
        responses={201: election_document_schema, 404: "", 400: ""},
    )
    def post(self, request: HttpRequest):
        """
        This is a test description.
        """
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

        device_token = request.headers.get("X-Device-ID")

        if not device_token:
            return Response(
                {"error": "Missing header: `X-Device-ID`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device = users_manager.get_or_create_device(device_token)

        election = manager.initiate_election(
            device, initiator_name, election_description
        )
        election_document = builders.build_election_document(election)

        return Response(election_document, status=status.HTTP_201_CREATED)


class ElectionDetailView(APIView):
    @swagger_auto_schema(
        operation_id="Get Election", responses={200: election_document_schema, 404: ""}
    )
    def get(self, request: HttpRequest, election_id: str):
        try:
            election = Election.objects.get(external_id=election_id)
        except Election.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        election_document = builders.build_election_document(election)

        return Response(election_document, status=status.HTTP_200_OK)


class ParticipantsView(APIView):
    device_id = openapi.Parameter(
        name="X-Device-ID",
        in_=openapi.IN_HEADER,
        description="Unique identifier for the device.",
        type=openapi.TYPE_STRING,
        required=True,
    )
    request_body = openapi.Schema(
        type="object",
        properties={
            "name": openapi.Schema(
                type="string",
                description="Name of the user joining the election.",
                example="Jane",
            )
        },
        required=["name"],
    )

    @swagger_auto_schema(
        operation_id="Create Participant",
        manual_parameters=[device_id],
        request_body=request_body,
        responses={201: "Null response", 404: "", 400: ""},
    )
    def post(self, request: HttpRequest, election_id: str):
        try:
            election = Election.objects.get(external_id=election_id)
        except Election.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get("name")

        if not name:
            return Response(
                {"error": "Missing parameter: `name`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_token = request.headers.get("X-Device-ID")

        if not device_token:
            return Response(
                {"error": "Missing header: `X-Device-ID`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device = users_manager.get_or_create_device(device_token)
        manager.create_participant_for_election(election, device, name)

        return Response({}, status=status.HTTP_201_CREATED)
