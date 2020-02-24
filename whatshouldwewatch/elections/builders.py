from whatshouldwewatch.elections.models import Election


def build_election_document(election: Election) -> dict:
    return {"id": election.external_id, "description": election.description}
