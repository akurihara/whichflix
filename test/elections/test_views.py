import datetime

from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APITestCase

from whichflix.elections.models import Candidate, Election, Participant, Vote
from whichflix.movies.models import Movie
from whichflix.users.models import Device
from test import factories
from test.elections import fixtures


class TestGetElectionDetailView(APITestCase):
    def tearDown(self):
        Vote.objects.all().delete()
        Candidate.objects.all().delete()
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()
        Movie.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_get_election(self):
        # Set up election.
        election = factories.create_election()
        candidate = factories.create_candidate(election, election.participants.first())
        Vote.objects.create(
            participant=election.participants.first(), candidate=candidate
        )

        url = reverse("election_detail", kwargs={"election_id": election.external_id})
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_GET_ELECTION_DETAIL
        )


class TestPutElectionDetailView(APITestCase):
    def tearDown(self):
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_put(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device=device)

        url = reverse("election_detail", kwargs={"election_id": election.external_id})
        title = "This is an updated test title."
        data = {"title": title}

        response = self.client.put(url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_UPDATE_ELECTION
        )

        # Verify election in database.
        election = Election.objects.filter(external_id=election.external_id).first()
        self.assertEqual(election.title, title)

    def test_put_elections_returns_error_when_device_header_is_missing(self):
        # Set up election.
        election = factories.create_election()

        url = reverse("election_detail", kwargs={"election_id": election.external_id})
        title = "This is an updated test title."
        data = {"title": title}

        response = self.client.put(url, data=data, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing header: `X-Device-ID`.")

    def test_put_elections_returns_error_when_title_is_missing(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device=device)

        url = reverse("election_detail", kwargs={"election_id": election.external_id})
        response = self.client.put(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `title`.")

    def test_put_elections_returns_error_when_device_is_not_initiator_of_election(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election()

        url = reverse("election_detail", kwargs={"election_id": election.external_id})
        title = "This is an updated test title."
        data = {"title": title}

        response = self.client.put(url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"], "The device is not the initiator of the election."
        )


class TestGetElectionsView(APITestCase):
    def setUp(self):
        self.url = reverse("elections")

    def tearDown(self):
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_get_elections(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}
        factories.create_election(device=device, external_id="abc123")
        factories.create_election(device=device, external_id="def456")

        response = self.client.get(self.url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), fixtures.EXPECTED_RESPONSE_GET_ELECTIONS)

    def test_get_elections_when_device_id_has_no_elections(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.get(self.url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"results": []})

    def test_get_elections_when_participant_is_deleted(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}
        election = factories.create_election(device=device, external_id="abc123")
        participant = election.participants.first()
        participant.deleted_at = datetime.datetime.now(tz=timezone.utc)
        participant.save()

        response = self.client.get(self.url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"results": []})

    def test_get_elections_returns_error_when_device_header_is_missing(self):
        response = self.client.get(self.url)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing header: `X-Device-ID`.")


class TestCreateElectionsView(APITestCase):
    def setUp(self):
        self.url = reverse("elections")

    def tearDown(self):
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_post_initiates_election(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        initiator_name = "John"
        title = "Movie night in Brooklyn!"
        data = {"title": title, "initiator_name": initiator_name}

        response = self.client.post(self.url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        self.assertDictEqual(response_json, fixtures.EXPECTED_RESPONSE_CREATE_ELECTION)
        external_id = response_json["id"]

        # Verify election in database.
        election = Election.objects.filter(external_id=external_id).first()
        self.assertIsNotNone(election)
        self.assertEqual(election.title, title)

        # Verify participant in database.
        self.assertEqual(election.participants.count(), 1)
        participant = election.participants.first()
        self.assertEqual(participant.name, initiator_name)
        self.assertTrue(participant.is_initiator)

    def test_post_creates_device_if_none_exists(self):
        initiator_name = "John"
        title = "This is a test title."
        data = {"title": title, "initiator_name": initiator_name}
        device_token = "new-device-token"
        headers = {"HTTP_X_DEVICE_ID": device_token}

        response = self.client.post(self.url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        self.assertIn("id", response_json)

        # Verify device in database.
        device = Device.objects.filter(device_token=device_token).first()
        self.assertIsNotNone(device)

        # Verify participant in database.
        election = Election.objects.get(external_id=response_json["id"])
        self.assertEqual(election.participants.count(), 1)
        participant = election.participants.first()
        self.assertEqual(participant.name, initiator_name)
        self.assertEqual(participant.device_id, device.id)
        self.assertTrue(participant.is_initiator)

    def test_post_returns_error_when_title_is_missing(self):
        # Set up device
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.post(
            self.url, data={"iniator_name": "John"}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `title`.")

    def test_post_returns_error_when_initiator_name_is_missing(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.post(
            self.url, data={"title": "This is a test title."}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `initiator_name`.")

    def test_post_returns_error_when_device_header_is_missing(self):
        response = self.client.post(
            self.url,
            data={"title": "This is a test title.", "initiator_name": "John"},
            format="json",
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing header: `X-Device-ID`.")


class TestCandidatesView(APITestCase):
    def tearDown(self):
        Candidate.objects.all().delete()
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()
        Movie.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_post_create_candidate(self):
        self.maxDiff = None
        # Set up device.
        device = Device.objects.create(device_token="abc123")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)
        movie = factories.create_movie(provider_id="1")

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(
            url, data={"movie_id": movie.id}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_CREATE_CANDIDATE
        )

        # Verify candidate in database.
        self.assertEqual(election.candidates.count(), 1)
        candidate = election.candidates.first()
        self.assertEqual(candidate.movie_id, movie.id)
        self.assertEqual(candidate.participant, election.participants.first())

    def test_post_returns_error_when_election_does_not_exist(self):
        url = reverse("candidates", kwargs={"election_id": "invalid_election_id"})
        response = self.client.post(url, data={"movie_id": "123"}, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 404)

    def test_post_returns_error_when_movie_id_is_missing(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `movie_id`.")

    def test_post_returns_error_when_device_header_is_missing(self):
        # Set up election
        election = factories.create_election()

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={"movie_id": "123"}, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing header: `X-Device-ID`.")

    def test_post_returns_error_when_participant_does_not_exist(self):
        headers = {"HTTP_X_DEVICE_ID": "invalid_device_id"}

        # Set up election.
        election = factories.create_election()

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(
            url, data={"movie_id": "123"}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Participant with the provided device ID does not exist in the election.",
        )

    def test_post_returns_error_when_movie_does_not_exist(self):
        # Set up device.
        device = Device.objects.create(device_token="abc123")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(
            url, data={"movie_id": "123"}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Movie does not exist.")

    def test_post_returns_error_when_participant_not_part_of_election(self):
        # Set up device.
        first_device = factories.create_device(device_token="abc123")
        second_device = factories.create_device(device_token="def456")
        headers = {"HTTP_X_DEVICE_ID": second_device.device_token}

        # Set up elections.
        first_election = factories.create_election(first_device, external_id="abc123")
        factories.create_election(second_device, external_id="def456")
        movie = factories.create_movie()

        url = reverse("candidates", kwargs={"election_id": first_election.external_id})
        response = self.client.post(
            url, data={"movie_id": movie.id}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Participant with the provided device ID does not exist in the election.",
        )

    def test_post_returns_error_when_candidate_already_exists(self):
        # Set up device.
        device = Device.objects.create(device_token="abc123")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)
        movie = factories.create_movie()
        Candidate.objects.create(
            election=election, participant=election.participants.first(), movie=movie
        )

        url = reverse("candidates", kwargs={"election_id": election.external_id})
        response = self.client.post(
            url, data={"movie_id": movie.id}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"], "A candidate for the movie provided already exists."
        )


class TestParticipantsView(APITestCase):
    def tearDown(self):
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_post_creates_participant(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election()
        name = "Jane"

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={"name": name}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_CREATE_PARTICIPANT
        )

        # Verify participant in database.
        participant = election.participants.filter(device=device).first()
        self.assertIsNotNone(participant)
        self.assertEqual(participant.name, name)
        self.assertEqual(participant.device_id, device.id)
        self.assertFalse(participant.is_initiator)

    def test_post_reactivates_deleted_participant(self):
        # Set up election.
        election = factories.create_election()
        name = "Jill"

        # Set up participant.
        device = Device.objects.create(device_token="some-device-token")
        participant = factories.create_participant(election, device, is_deleted=True)
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={"name": name}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)

        # Verify participant in database.
        participant = election.participants.filter(device=device).first()
        self.assertIsNotNone(participant)
        self.assertIsNone(participant.deleted_at)
        self.assertEqual(participant.name, name)

    def test_post_returns_error_when_election_does_not_exist(self):
        url = reverse("participants", kwargs={"election_id": "invalid_election_id"})
        response = self.client.post(url, data={"name": "Jane"}, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 404)

    def test_post_returns_error_when_name_is_missing(self):
        # Set up device.
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election()

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `name`.")

    def test_post_returns_error_when_device_header_is_missing(self):
        # Set up election
        election = factories.create_election()

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.post(url, data={"name": "Jane"}, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing header: `X-Device-ID`.")

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_delete_removes_participant(self):
        # Set up election.
        election = factories.create_election()

        # Set up participant.
        device = Device.objects.create(device_token="some-device-token")
        participant = factories.create_participant(election, device)
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_CREATE_ELECTION
        )

        # Verify participant in database.
        participant = election.participants.filter(device=device).first()
        self.assertIsNotNone(participant.deleted_at)

    def test_delete_returns_error_when_election_does_not_exist(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}
        url = reverse("participants", kwargs={"election_id": "invalid_election_id"})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 404)

    def test_delete_returns_error_is_participant_already_deleted(self):
        # Set up election.
        election = factories.create_election()

        # Set up participant.
        device = Device.objects.create(device_token="some-device-token")
        factories.create_participant(election, device, is_deleted=True)
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        url = reverse("participants", kwargs={"election_id": election.external_id})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Participant with the provided device ID does not exist in the election.",
        )


class TestVotesView(APITestCase):
    def tearDown(self):
        Vote.objects.all().delete()
        Candidate.objects.all().delete()
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()
        Movie.objects.all().delete()

    def test_post_create_vote(self):
        # Set up device.
        device = Device.objects.create(device_token="abc123")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)
        candidate = factories.create_candidate(election, election.participants.first())

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)

        # Verify vote in database.
        self.assertEqual(candidate.votes.count(), 1)
        self.assertEqual(
            candidate.votes.first().participant, election.participants.first()
        )

    def test_post_reactivates_deleted_vote(self):
        # Set up election.
        election = factories.create_election()
        participant = election.participants.first()
        candidate = factories.create_candidate(election, participant)
        vote = Vote.objects.create(
            participant=participant,
            candidate=candidate,
            deleted_at=datetime.datetime.now(tz=timezone.utc),
        )
        headers = {"HTTP_X_DEVICE_ID": participant.device.device_token}

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 201)

        # Verify vote in database.
        vote.refresh_from_db()
        self.assertIsNone(vote.deleted_at)

    def test_post_returns_error_when_candidate_does_not_exist(self):
        url = reverse("votes", kwargs={"candidate_id": "123"})
        response = self.client.post(url, data={}, format="json")

        # Verify response.
        self.assertEqual(response.status_code, 404)

    def test_post_returns_error_when_participant_not_part_of_election(self):
        # Set up device.
        first_device = factories.create_device(device_token="abc123")
        second_device = factories.create_device(device_token="def456")
        headers = {"HTTP_X_DEVICE_ID": second_device.device_token}

        # Set up elections.
        first_election = factories.create_election(first_device, external_id="abc123")
        candidate = factories.create_candidate(
            first_election, first_election.participants.first()
        )
        factories.create_election(second_device, external_id="def456")

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Participant with the provided device ID does not exist in the election.",
        )

    def test_post_returns_error_when_participant_already_voted_for_candidate(self):
        # Set up device.
        device = Device.objects.create(device_token="abc123")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        # Set up election.
        election = factories.create_election(device)
        candidate = factories.create_candidate(election, election.participants.first())
        Vote.objects.create(
            participant=election.participants.first(), candidate=candidate
        )

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.post(url, data={}, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "The participant has already voted for the candidate.",
        )

    @freeze_time("2020-02-25 23:21:34", tz_offset=-5)
    def test_delete_removes_vote(self):
        # Set up election.
        election = factories.create_election()
        participant = election.participants.first()
        candidate = factories.create_candidate(election, participant)
        vote = Vote.objects.create(participant=participant, candidate=candidate)
        headers = {"HTTP_X_DEVICE_ID": participant.device.device_token}

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(), fixtures.EXPECTED_RESPONSE_CREATE_CANDIDATE
        )

        # Verify vote in database.
        vote.refresh_from_db()
        self.assertIsNotNone(vote.deleted_at)

    def test_delete_returns_error_when_candidate_does_not_exist(self):
        # Set up election.
        election = factories.create_election()
        participant = election.participants.first()
        headers = {"HTTP_X_DEVICE_ID": participant.device.device_token}

        url = reverse("votes", kwargs={"candidate_id": "123"})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 404)

    def test_delete_returns_error_when_participant_does_not_exist(self):
        # Set up election.
        election = factories.create_election()
        participant = election.participants.first()
        candidate = factories.create_candidate(election, participant)
        Vote.objects.create(participant=participant, candidate=candidate)
        headers = {"HTTP_X_DEVICE_ID": "invalid_device_id"}

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Participant with the provided device ID does not exist in the election.",
        )

    def test_delete_returns_error_if_vote_already_deleted(self):
        # Set up election.
        election = factories.create_election()
        participant = election.participants.first()
        candidate = factories.create_candidate(election, participant)
        Vote.objects.create(
            participant=participant,
            candidate=candidate,
            deleted_at=datetime.datetime.now(tz=timezone.utc),
        )
        headers = {"HTTP_X_DEVICE_ID": participant.device.device_token}

        url = reverse("votes", kwargs={"candidate_id": candidate.id})
        response = self.client.delete(url, **headers)

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"],
            "Vote with the provided device ID does not exist for the candidate.",
        )
