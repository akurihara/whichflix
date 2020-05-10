from drf_yasg import openapi

from whichflix.movies import schemas as movie_schemas

#
# Parameters
#


DEVICE_ID_PARAMETER = openapi.Parameter(
    name="X-Device-ID",
    in_=openapi.IN_HEADER,
    description="A unique identifier for the device.",
    type=openapi.TYPE_STRING,
    required=True,
)


#
# Request bodies
#


CREATE_CANDIDATE_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "movie_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="A unique identifier for a movie.",
            example="nygr37",
        )
    },
    required=["movie_id"],
)

CREATE_ELECTION_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        ),
        "initiator_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the user initiating the election.",
            example="John",
        ),
    },
    required=["title", "initiator_name"],
)

UPDATE_ELECTION_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        )
    },
    required=["title"],
)

CREATE_PARTICIPANT_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the user joining the election.",
            example="Jane",
        )
    },
    required=["name"],
)


#
# Documents
#


PARTICIPANT_DOCUMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="A unique identifier for the participant.",
            example="123",
        ),
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the participant.",
            example="John",
        ),
        "is_initiator": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Whether the participant initiated the election.",
        ),
    },
)

CANDIDATE_ACTIONS_DOCUMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    nullable=True,
    properties={
        "can_vote": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Whether the user is able to voted for the candidate.",
        ),
        "can_remove_vote": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Whether the user is able to remove their vote for the candidate.",
        ),
        "can_delete": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Whether the user is able to delete the candidate.",
        ),
    },
)

CANDIDATE_DOCUMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "actions": CANDIDATE_ACTIONS_DOCUMENT_SCHEMA,
        "id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="A unique identifier for the candidate.",
            example="456",
        ),
        "movie": movie_schemas.MOVIE_DOCUMENT_SCHEMA,
        "vote_count": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="The number of votes the candidate has earned from active participants.",
            example=5,
        ),
        "voting_participants": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="List of active participants who voted for this candidate.",
            items=PARTICIPANT_DOCUMENT_SCHEMA,
        ),
    },
)

ELECTION_DOCUMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="A unique identifier for the election.",
            example="nygr37",
        ),
        "title": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Timestamp of the election's creation in ISO 8601 format.",
            example="2020-02-25T23:21:34+00:00",
        ),
        "candidates": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="List of movie candidates and their voters.",
            items=CANDIDATE_DOCUMENT_SCHEMA,
        ),
        "participants": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="List of active participants in the election.",
            items=PARTICIPANT_DOCUMENT_SCHEMA,
        ),
    },
)

GET_ELECTIONS_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="List of elections the device is currently participating in.",
            items=ELECTION_DOCUMENT_SCHEMA,
        )
    },
)
