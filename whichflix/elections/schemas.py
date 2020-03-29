from drf_yasg import openapi

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
    type="object",
    properties={
        "movie_id": openapi.Schema(
            type="string",
            description="A unique identifier for a movie.",
            example="nygr37",
        )
    },
    required=["movie_id"],
)

CREATE_ELECTION_REQUEST_BODY = openapi.Schema(
    type="object",
    properties={
        "title": openapi.Schema(
            type="string",
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        ),
        "initiator_name": openapi.Schema(
            type="string",
            description="Name of the user initiating the election.",
            example="John",
        ),
    },
    required=["title", "initiator_name"],
)

UPDATE_ELECTION_REQUEST_BODY = openapi.Schema(
    type="object",
    properties={
        "title": openapi.Schema(
            type="string",
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        )
    },
    required=["title"],
)

CREATE_PARTICIPANT_REQUEST_BODY = openapi.Schema(
    type="object",
    properties={
        "name": openapi.Schema(
            type="string",
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
    type="object",
    properties={
        "id": openapi.Schema(
            type="string",
            description="A unique identifier for the participant.",
            example="123",
        ),
        "name": openapi.Schema(
            type="string", description="Name of the participant.", example="John"
        ),
        "is_initiator": openapi.Schema(
            type="boolean",
            description="Whether the participant initiated the election.",
        ),
    },
)

CANDIDATE_DOCUMENT_SCHEMA = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(
            type="string",
            description="A unique identifier for the candidate.",
            example="456",
        ),
        "vote_count": openapi.Schema(
            type="integer",
            description="The number of votes the candidate has earned from active participants.",
            example=5,
        ),
        "voting_participants": openapi.Schema(
            type="array",
            description="List of active participants who voted for this candidate.",
            items=PARTICIPANT_DOCUMENT_SCHEMA,
        ),
    },
)

ELECTION_DOCUMENT_SCHEMA = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(
            type="string",
            description="A unique identifier for the election.",
            example="nygr37",
        ),
        "title": openapi.Schema(
            type="string",
            description="Description of the election.",
            example="Movie night in Brooklyn!",
        ),
        "created_at": openapi.Schema(
            type="string",
            description="Timestamp of the election's creation in ISO 8601 format.",
            example="2020-02-25T23:21:34+00:00",
        ),
        "candidates": openapi.Schema(
            type="array",
            description="List of movie candidates and their voters.",
            items=CANDIDATE_DOCUMENT_SCHEMA,
        ),
        "participants": openapi.Schema(
            type="array",
            description="List of active participants in the election.",
            items=PARTICIPANT_DOCUMENT_SCHEMA,
        ),
    },
)

GET_ELECTIONS_SCHEMA = openapi.Schema(
    type="object",
    properties={
        "results": openapi.Schema(
            type="array",
            description="List of elections the device is currently participating in.",
            items=ELECTION_DOCUMENT_SCHEMA,
        )
    },
)
