from typing import Optional

from whichflix.movies import constants
from whichflix.movies.models import TMDBMovie


def build_movie_document(tmdb_movie: TMDBMovie, tmdb_configuration: dict) -> dict:
    genres = [constants.GENRE_ID_TO_NAME[genre_id] for genre_id in tmdb_movie.genre_ids]

    return {
        "id": str(tmdb_movie._id),
        "title": tmdb_movie.title,
        "image_url": build_image_url(tmdb_movie, tmdb_configuration),
        "description": tmdb_movie.overview,
        "release_year": tmdb_movie.release_date[:4],
        "genres": genres,
    }


def build_image_url(tmdb_movie: TMDBMovie, tmdb_configuration: dict) -> Optional[str]:
    if not tmdb_movie.poster_path:
        return None

    return "{base_url}{image_size}{poster_path}".format(
        base_url=tmdb_configuration["images"]["secure_base_url"],
        image_size=tmdb_configuration["images"]["poster_sizes"][4],
        poster_path=tmdb_movie.poster_path,
    )
