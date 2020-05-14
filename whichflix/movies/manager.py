import json
from typing import List, Optional

from whichflix.clients import redis_client
from whichflix.movies import constants
from whichflix.movies.models import Movie, TMDBMovie
from whichflix.movies.tmdb_client import tmdb


def get_movie_by_id(movie_id: str) -> Optional[Movie]:
    try:
        movie = Movie.objects.get(id=int(movie_id))
    except Movie.DoesNotExist:
        movie = None

    return movie


def create_movie(provider_id: str, provider_slug: str) -> Movie:
    movie = Movie.objects.create(provider_id=provider_id, provider_slug=provider_slug)

    return movie


def search_movies(query: str) -> List[TMDBMovie]:
    search = tmdb.Search()
    response = search.movie(query=query)
    tmdb_movies = [TMDBMovie.from_tmdb_result(result) for result in response["results"]]

    return tmdb_movies


def get_tmdb_configuration() -> dict:
    response = _get_cached_configuration()

    if response is not None:
        # Cache hit.
        return response

    # Cache miss.
    config = tmdb.Configuration()
    response = config.info()

    # Insert the venue detail response into the cache.
    twenty_four_hours_in_seconds = 60 * 60 * 24
    redis_client.set(
        constants.TMDB_CONFIGURATION_KEY,
        json.dumps(response),
        ex=twenty_four_hours_in_seconds,
    )

    return response


def _get_cached_configuration() -> Optional[dict]:
    response_string = redis_client.get(constants.TMDB_CONFIGURATION_KEY)

    return json.loads(response_string) if response_string else None
