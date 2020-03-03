from whatshouldwewatch.elections.models import Election


def build_election_document(election: Election) -> dict:
    return {
        "id": election.external_id,
        "title": election.title,
        "created_at": election.created_at.isoformat(),
        "candidates": [
            {
                "id": str(candidate.id),
                "vote_count": candidate.votes.count(),
                "voting_participants": [
                    {
                        "id": str(vote.participant.id),
                        "name": vote.participant.name,
                        "is_initiator": vote.participant.is_initiator,
                    }
                    for vote in candidate.votes.all()
                ],
            }
            for candidate in election.candidates.all()
        ],
    }
