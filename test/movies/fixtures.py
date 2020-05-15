#
# Responses from TheMovieDatabase
#


CONFIGURATION_RESPONSE = {
    "images": {
        "base_url": "http://image.tmdb.org/t/p/",
        "secure_base_url": "https://image.tmdb.org/t/p/",
        "backdrop_sizes": ["w300", "w780", "w1280", "original"],
        "logo_sizes": ["w45", "w92", "w154", "w185", "w300", "w500", "original"],
        "poster_sizes": ["w92", "w154", "w185", "w342", "w500", "w780", "original"],
        "profile_sizes": ["w45", "w185", "h632", "original"],
        "still_sizes": ["w92", "w185", "w300", "original"],
    },
    "change_keys": [],
}

SEARCH_MOVIES_RESPONSE = {
    "page": 1,
    "total_results": 1,
    "total_pages": 1,
    "results": [
        {
            "popularity": 36.362,
            "vote_count": 16910,
            "video": False,
            "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "id": 603,
            "adult": False,
            "backdrop_path": "/ByDf0zjLSumz1MP1cDEo2JWVtU.jpg",
            "original_language": "en",
            "original_title": "The Matrix",
            "genre_ids": [28, 878],
            "title": "The Matrix",
            "vote_average": 8.1,
            "overview": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
            "release_date": "1999-03-30",
        }
    ],
}

MOVIE_INFO_RESPONSE = {
    "adult": False,
    "backdrop_path": "/ByDf0zjLSumz1MP1cDEo2JWVtU.jpg",
    "belongs_to_collection": {
        "id": 2344,
        "name": "The Matrix Collection",
        "poster_path": "/lh4aGpd3U9rm9B8Oqr6CUgQLtZL.jpg",
        "backdrop_path": "/bRm2DEgUiYciDw3myHuYFInD7la.jpg",
    },
    "budget": 63000000,
    "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
    "homepage": "http://www.warnerbros.com/matrix",
    "id": 603,
    "imdb_id": "tt0133093",
    "original_language": "en",
    "original_title": "The Matrix",
    "overview": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
    "popularity": 40.705,
    "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "production_companies": [
        {
            "id": 79,
            "logo_path": "/tpFpsqbleCzEE2p5EgvUq6ozfCA.png",
            "name": "Village Roadshow Pictures",
            "origin_country": "US",
        },
        {
            "id": 372,
            "logo_path": None,
            "name": "Groucho II Film Partnership",
            "origin_country": "",
        },
        {
            "id": 1885,
            "logo_path": "/xlvoOZr4s1PygosrwZyolIFe5xs.png",
            "name": "Silver Pictures",
            "origin_country": "US",
        },
        {
            "id": 174,
            "logo_path": "/IuAlhI9eVC9Z8UQWOIDdWRKSEJ.png",
            "name": "Warner Bros. Pictures",
            "origin_country": "US",
        },
    ],
    "production_countries": [
        {"iso_3166_1": "AU", "name": "Australia"},
        {"iso_3166_1": "US", "name": "United States of America"},
    ],
    "release_date": "1999-03-30",
    "revenue": 463517383,
    "runtime": 136,
    "spoken_languages": [{"iso_639_1": "en", "name": "English"}],
    "status": "Released",
    "tagline": "Welcome to the Real World.",
    "title": "The Matrix",
    "video": False,
    "vote_average": 8.1,
    "vote_count": 16915,
}


#
# Expected responses from WhichFlix
#


EXPECTED_RESPONSE_SEARCH_MOVIES = {
    "results": [
        {
            "id": "603",
            "title": "The Matrix",
            "image_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "description": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
            "release_year": "1999",
            "genres": ["Action", "Science Fiction"],
        }
    ]
}
