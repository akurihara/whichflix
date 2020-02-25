from typing import Optional

from whatshouldwewatch.movies.models import Movie


def get_movie_by_id(movie_id: str) -> Optional[Movie]:
    try:
        movie = Movie.objects.get(id=int(movie_id))
    except Movie.DoesNotExist:
        movie = None

    return movie
