from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from whichflix.movies import manager


class MoviesSearchView(APIView):
    def get(self, request: HttpRequest) -> Response:
        """
        Search for movies by genre name or movie title.
        """
        query = request.GET.get("query")
        results = manager.search_movies(query)
        response_body = results

        return Response(response_body, status=status.HTTP_200_OK)
