from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from whatshouldwewatch.elections import builders, errors, manager, schemas
from whatshouldwewatch.elections.models import Election, Candidate
from whatshouldwewatch.movies import manager as movies_manager
from whatshouldwewatch.users import manager as users_manager


class CandidatesView(APIView):
    @swagger_auto_schema(
        operation_id="Create Candidate",
        manual_parameters=[schemas.DEVICE_ID_PARAMETER],
        request_body=schemas.CREATE_CANDIDATE_REQUEST_BODY,
        responses={201: "Null response", 404: ""},
    )
    def post(self, request: HttpRequest, election_id: str) -> Response:
        """
        Create a new movie candidate. Called when a user finds a movie they want to suggest
        to the group.
        """
        try:
            election = Election.objects.get(external_id=election_id)
        except Election.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        device_token = request.headers.get("X-Device-ID")

        if not device_token:
            return Response(
                {"error": "Missing header: `X-Device-ID`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participant = manager.get_participant_by_device_token(device_token)

        if not participant:
            return Response(
                {"error": "Participant with the provided device ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie_id = request.data.get("movie_id")

        if not movie_id:
            return Response(
                {"error": "Missing parameter: `movie_id`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie = movies_manager.get_movie_by_id(movie_id)

        if not movie:
            return Response(
                {"error": "Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager.create_candidate_for_election(election, participant, movie)
        except (
            errors.ParticipantNotPartOfElectionError,
            errors.CandidateAlreadyExistsError,
        ) as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_201_CREATED)


class ElectionsView(APIView):
    @swagger_auto_schema(
        operation_id="Create Election",
        manual_parameters=[schemas.DEVICE_ID_PARAMETER],
        request_body=schemas.CREATE_ELECTION_REQUEST_BODY,
        responses={201: schemas.ELECTION_DOCUMENT_SCHEMA, 404: "", 400: ""},
    )
    def post(self, request: HttpRequest) -> Response:
        """
        Create a new election.
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
        operation_id="Get Election",
        responses={200: schemas.ELECTION_DOCUMENT_SCHEMA, 404: ""},
    )
    def get(self, request: HttpRequest, election_id: str) -> Response:
        """
        Get information about a single election, including participants and candidates.
        """
        election = manager.get_election_and_related_objects(election_id)

        if not election:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        election_document = builders.build_election_document(election)

        return Response(election_document, status=status.HTTP_200_OK)


class ParticipantsView(APIView):
    @swagger_auto_schema(
        operation_id="Create Participant",
        manual_parameters=[schemas.DEVICE_ID_PARAMETER],
        request_body=schemas.CREATE_PARTICIPANT_REQUEST_BODY,
        responses={201: "Null response", 404: "", 400: ""},
    )
    def post(self, request: HttpRequest, election_id: str) -> Response:
        """
        Create a new participant for an existing election. Called when a user clicks an
        election link and is prompted to enter their name and join the election.
        """
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


class VotesView(APIView):
    @swagger_auto_schema(
        operation_id="Cast Vote",
        manual_parameters=[schemas.DEVICE_ID_PARAMETER],
        responses={201: "Null response", 404: "", 400: ""},
    )
    def post(self, request: HttpRequest, candidate_id: str) -> Response:
        """
        Cast a vote for one of the candidates in an election.
        """
        try:
            candidate = Candidate.objects.get(id=int(candidate_id))
        except Candidate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        device_token = request.headers.get("X-Device-ID")

        if not device_token:
            return Response(
                {"error": "Missing header: `X-Device-ID`."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participant = manager.get_participant_by_device_token(device_token)

        if not participant:
            return Response(
                {"error": "Participant with the provided device ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            manager.cast_vote_for_candidate(participant, candidate)
        except (
            errors.ParticipantNotPartOfElectionError,
            errors.ParticipantAlreadyVotedForCandidate,
        ) as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
