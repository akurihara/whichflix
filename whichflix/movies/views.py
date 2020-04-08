from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# from whichflix.movies import manager
from whichflix.movies import constants, schemas


class MoviesSearchView(APIView):
    @swagger_auto_schema(
        operation_id="Search Movies",
        manual_parameters=[schemas.SEARCH_QUERY_PARAMETER],
        responses={200: schemas.SEARCH_MOVIES_RESPONSE_BODY},
    )
    def get(self, request: HttpRequest) -> Response:
        """
        Search for movies by genre name or movie title.
        """
        # query = request.GET.get("query")
        # results = manager.search_movies(query)
        # response_body = results

        return Response(constants.FIXTURE_RESULTS, status=status.HTTP_200_OK)
