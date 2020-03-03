from unittest.mock import ANY

#
# Expected responses from WhichFlix
#


EXPECTED_RESPONSE_GET_ELECTION_DETAIL = {
    "candidates": [
        {
            "id": ANY,
            "vote_count": 1,
            "voting_participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
        }
    ],
    "created_at": "2020-02-25T23:21:34+00:00",
    "title": "Movie night in Brooklyn!",
    "id": "abc123",
}

EXPECTED_RESPONSE_GET_ELECTIONS = {
    "results": [
        {
            "candidates": [],
            "created_at": "2020-02-25T23:21:34+00:00",
            "title": "Movie night in Brooklyn!",
            "id": "abc123",
        },
        {
            "candidates": [],
            "created_at": "2020-02-25T23:21:34+00:00",
            "title": "Movie night in Brooklyn!",
            "id": "def456",
        },
    ]
}
