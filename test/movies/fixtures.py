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
