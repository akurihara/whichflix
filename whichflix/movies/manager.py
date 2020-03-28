from typing import List, Optional

from whichflix.movies.models import Movie
from whichflix.movies.tmdb_client import tmdb


def get_movie_by_id(movie_id: str) -> Optional[Movie]:
    try:
        movie = Movie.objects.get(id=int(movie_id))
    except Movie.DoesNotExist:
        movie = None

    return movie


def search_movies(query: str) -> List[dict]:
    search = tmdb.Search()
    response = search.movie(query=query)

    return response
