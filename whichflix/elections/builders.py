from whichflix.elections.models import Election


def build_election_document(election: Election) -> dict:
    return {
        "id": election.external_id,
        "title": election.title,
        "created_at": election.created_at.isoformat(),
        "participants": [
            {
                "id": str(participant.id),
                "name": participant.name,
                "is_initiator": participant.is_initiator,
            }
            for participant in election.participants.order_by("id")
            .order_by("name")
            .all()
            if participant.deleted_at is None
        ],
        "candidates": [
            {
                "id": str(candidate.id),
                "vote_count": candidate.votes.filter(
                    participant__deleted_at__isnull=True
                ).count(),
                "voting_participants": [
                    {
                        "id": str(vote.participant.id),
                        "name": vote.participant.name,
                        "is_initiator": vote.participant.is_initiator,
                    }
                    for vote in candidate.votes.filter(
                        participant__deleted_at__isnull=True
                    ).all()
                ],
            }
            for candidate in election.candidates.all()
        ],
    }
