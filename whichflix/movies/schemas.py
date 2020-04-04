from drf_yasg import openapi

#
# Parameters
#


SEARCH_QUERY_PARAMETER = openapi.Parameter(
    name="query",
    in_=openapi.IN_QUERY,
    description="The search term used to find movies.",
    type=openapi.TYPE_STRING,
    required=True,
)


#
# Documents
#


MOVIE_DOCUMENT_SCHEMA = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(
            type="string",
            description="A unique identifier for the movie.",
            example="123",
        ),
        "title": openapi.Schema(
            type="string", description="Title of the movie.", example="Interstellar"
        ),
        "image_url": openapi.Schema(
            type="string",
            description="Link to the movie poster image.",
            example="https://image.tmdb.org/t/p/w500/nBNZadXqJSdt05SHLqgT0HuC5Gm.jpg",
        ),
        "description": openapi.Schema(
            type="string",
            description="Synopsis of the movie plot.",
            example="Interstellar chronicles the adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        ),
        "release_year": openapi.Schema(
            type="string",
            description="Year the movie was released in theaters.",
            example="2014",
        ),
        "genres": openapi.Schema(
            type="array",
            description="List of genres associated with the movie.",
            items=openapi.Schema(type="string", example="Science Fiction"),
        ),
    },
)


#
# Response Bodies
#


SEARCH_MOVIES_RESPONSE_BODY = openapi.Schema(
    type="object",
    properties={
        "results": openapi.Schema(
            type="array",
            description="List of movies matching the search term.",
            items=MOVIE_DOCUMENT_SCHEMA,
        )
    },
)
