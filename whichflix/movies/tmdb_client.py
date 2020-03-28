import os

import tmdbsimple as tmdb

tmdb.API_KEY = os.getenv("TMDB_API_KEY")
