from hashids import Hashids


hashids = Hashids(
    alphabet="abcdefghijklmnopqrstuvwxyz1234567890",
    min_length=6,
    salt="whatshouldwewatch",
)


def generate_external_id(internal_id):
    return hashids.encode(internal_id)
