#
# Movies
#

MOVIE_QUERY_MINIMUM_LENGTH = 3


GENRE_ID_TO_NAME = {
    12: "Adventure",
    14: "Fantasy",
    16: "Animation",
    18: "Drama",
    27: "Horror",
    28: "Action",
    35: "Comedy",
    36: "History",
    37: "Western",
    53: "Thriller",
    80: "Crime",
    99: "Documentary",
    878: "Science Fiction",
    9648: "Mystery",
    10402: "Music",
    10749: "Romance",
    10751: "Family",
    10752: "War",
    10770: "TV Movie",
}


#
# Redis keys
#


TMDB_CONFIGURATION_KEY = "movies:themoviedatabase:configuration"
TMDB_MOVIE_INFO_KEY = "movies:themoviedatabase:movie:{movie_id}"
