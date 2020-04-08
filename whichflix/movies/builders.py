from whichflix.movies import constants
from whichflix.movies.models import Movie


def build_movie_document(movie: Movie) -> dict:
    return constants.FIXTURE_RESULTS_MAP.get(movie.provider_id, {})
