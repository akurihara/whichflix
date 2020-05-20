import json
from typing import List, Optional

import requests

from whichflix.clients import redis_client
from whichflix.movies import builders, constants, errors
from whichflix.movies.models import TMDBMovie
from whichflix.movies.tmdb_client import tmdb


def get_movie_document(movie_id: str) -> dict:
    tmdb_movie = get_tmdb_movie_by_id(movie_id)
    tmdb_configuration = get_tmdb_configuration()

    return builders.build_movie_document(tmdb_movie, tmdb_configuration)


def get_tmdb_movie_by_id(tmdb_movie_id: str) -> TMDBMovie:
    movie_info = _get_cached_movie_info(tmdb_movie_id)

    if movie_info is not None:
        # Cache hit.
        return TMDBMovie.from_tmdb_movie_info(movie_info)

    # Cache miss.
    movie_request = tmdb.Movies(int(tmdb_movie_id))

    try:
        movie_info = movie_request.info()
    except requests.exceptions.HTTPError:
        raise errors.TMDBMovieDoesNotExistError

    # Insert the movie info response into the cache.
    twenty_four_hours_in_seconds = 60 * 60 * 24
    redis_client.set(
        constants.TMDB_MOVIE_INFO_KEY.format(movie_id=tmdb_movie_id),
        json.dumps(movie_info),
        ex=twenty_four_hours_in_seconds,
    )

    return TMDBMovie.from_tmdb_movie_info(movie_info)


def _get_cached_movie_info(tmdb_movie_id: str) -> Optional[dict]:
    key = constants.TMDB_MOVIE_INFO_KEY.format(movie_id=tmdb_movie_id)
    response_string = redis_client.get(key)

    return json.loads(response_string) if response_string else None


def search_movies(query: str) -> List[TMDBMovie]:
    search = tmdb.Search()
    response = search.movie(query=query)
    tmdb_movies = [
        TMDBMovie.from_tmdb_movie_result(result) for result in response["results"]
    ]

    return tmdb_movies


def get_tmdb_configuration() -> dict:
    response = _get_cached_configuration()

    if response is not None:
        # Cache hit.
        return response

    # Cache miss.
    config = tmdb.Configuration()
    response = config.info()

    # Insert the configuration response into the cache.
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
