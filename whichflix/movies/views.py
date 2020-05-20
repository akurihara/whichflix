from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from whichflix.movies import builders, constants, manager, schemas


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
        query = request.GET.get("query")

        if len(query) < constants.MOVIE_QUERY_MINIMUM_LENGTH:
            return Response({"results": []}, status=status.HTTP_200_OK)

        tmdb_movies = manager.search_movies(query)
        tmdb_configuration = manager.get_tmdb_configuration()

        response_body = {
            "results": [
                builders.build_movie_document(tmdb_movie, tmdb_configuration)
                for tmdb_movie in tmdb_movies
            ]
        }

        return Response(response_body, status=status.HTTP_200_OK)
