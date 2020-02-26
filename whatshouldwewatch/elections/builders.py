from whatshouldwewatch.elections.models import Election


def build_election_document(election: Election) -> dict:
    return {
        "id": election.external_id,
        "description": election.description,
        "created_at": election.created_at.isoformat(),
        "participants": [
            {
                "id": str(participant.id),
                "name": participant.name,
                "is_initiator": participant.is_initiator,
            }
            for participant in election.participants.all()
        ],
        "candidates": [
            {
                "participant_id": str(candidate.participant.id),
                "movie_id": str(candidate.movie.id),
                "vote_count": candidate.votes.count(),
            }
            for candidate in election.candidates.all()
        ],
    }
