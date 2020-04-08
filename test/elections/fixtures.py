from unittest.mock import ANY

#
# Expected responses from WhichFlix
#


EXPECTED_RESPONSE_GET_ELECTION_DETAIL = {
    "candidates": [
        {
            "id": ANY,
            "movie": {
                "id": "1",
                "title": "The Avengers",
                "image_url": "https://image.tmdb.org/t/p/w500/cezWGskPY5x7GaglTTRN4Fugfb8.jpg",
                "description": "When an unexpected enemy emerges and threatens global safety and security, Nick Fury, director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster. Spanning the globe, a daring recruitment effort begins!",
                "release_year": "2012",
                "genres": ["Action", "Adventure", "Science Fiction"],
            },
            "vote_count": 1,
            "voting_participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
        }
    ],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
    "title": "Movie night in Brooklyn!",
    "id": "abc123",
}

EXPECTED_RESPONSE_CREATE_ELECTION = {
    "candidates": [],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
    "title": "Movie night in Brooklyn!",
    "id": ANY,
}

EXPECTED_RESPONSE_UPDATE_ELECTION = {
    "candidates": [],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
    "title": "This is an updated test title.",
    "id": "abc123",
}

EXPECTED_RESPONSE_GET_ELECTIONS = {
    "results": [
        {
            "candidates": [],
            "created_at": "2020-02-25T23:21:34+00:00",
            "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
            "title": "Movie night in Brooklyn!",
            "id": "abc123",
        },
        {
            "candidates": [],
            "created_at": "2020-02-25T23:21:34+00:00",
            "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
            "title": "Movie night in Brooklyn!",
            "id": "def456",
        },
    ]
}

EXPECTED_RESPONSE_CREATE_PARTICIPANT = {
    "candidates": [],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [
        {"id": ANY, "is_initiator": False, "name": "Jane"},
        {"id": ANY, "is_initiator": True, "name": "John"},
    ],
    "title": "Movie night in Brooklyn!",
    "id": "abc123",
}

EXPECTED_RESPONSE_CREATE_CANDIDATE = {
    "candidates": [
        {
            "id": ANY,
            "movie": {
                "id": "1",
                "title": "The Avengers",
                "image_url": "https://image.tmdb.org/t/p/w500/cezWGskPY5x7GaglTTRN4Fugfb8.jpg",
                "description": "When an unexpected enemy emerges and threatens global safety and security, Nick Fury, director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster. Spanning the globe, a daring recruitment effort begins!",
                "release_year": "2012",
                "genres": ["Action", "Adventure", "Science Fiction"],
            },
            "vote_count": 0,
            "voting_participants": [],
        }
    ],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
    "title": "Movie night in Brooklyn!",
    "id": "abc123",
}
