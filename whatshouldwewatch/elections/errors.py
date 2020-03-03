class ParticipantNotPartOfElectionError(Exception):
    message = "The participant is not part of the election."


class CandidateAlreadyExistsError(Exception):
    message = "A candidate for the movie provided already exists."


class ParticipantAlreadyVotedForCandidate(Exception):
    message = "The participant has already voted for the candidate."


class DeviceDidNotInitiateElectionError(Exception):
    message = "The device is not the initiator of the election."
