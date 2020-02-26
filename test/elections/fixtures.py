from unittest.mock import ANY

#
# Expected responses from WhichFlix
#


EXPECTED_RESPONSE_ELECTION = {
    "candidates": [{"movie_id": "4", "participant_id": ANY, "vote_count": 1}],
    "created_at": "2020-02-25T23:21:34+00:00",
    "description": "Movie night in Brooklyn!",
    "id": "abc123",
    "participants": [{"id": ANY, "is_initiator": True, "name": "John"}],
}
