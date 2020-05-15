from unittest.mock import ANY

#
# Expected responses from WhichFlix
#


MOVIE_DOCUMENT_THE_MATRIX = {
    "id": "603",
    "title": "The Matrix",
    "image_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "description": "Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.",
    "release_year": "1999",
    "genres": ["Action", "Science Fiction"],
}

EXPECTED_RESPONSE_GET_ELECTION_DETAIL = {
    "candidates": [
        {
            "id": ANY,
            "actions": {"can_vote": False, "can_remove_vote": True, "can_delete": True},
            "movie": MOVIE_DOCUMENT_THE_MATRIX,
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
            "actions": {"can_vote": True, "can_remove_vote": False, "can_delete": True},
            "movie": MOVIE_DOCUMENT_THE_MATRIX,
            "vote_count": 0,
            "voting_participants": [],
        }
    ],
    "created_at": "2020-02-25T23:21:34+00:00",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
    "title": "Movie night in Brooklyn!",
    "id": "abc123",
}

EXPECTED_RESPONSE_CREATE_VOTE = {
    "actions": {"can_vote": False, "can_remove_vote": True, "can_delete": True},
    "id": ANY,
    "movie": MOVIE_DOCUMENT_THE_MATRIX,
    "vote_count": 1,
    "voting_participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
}

EXPECTED_RESPONSE_DELETE_VOTE = {
    "actions": {"can_vote": True, "can_remove_vote": False, "can_delete": True},
    "id": ANY,
    "movie": MOVIE_DOCUMENT_THE_MATRIX,
    "vote_count": 0,
    "voting_participants": [],
}
