from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Crew
from airport.serializers import CrewSerializer

CREW_URL = reverse("airport:crew-list")


def sample_crew(**params) -> Crew:
    defaults = {
        "first_name": "Max",
        "last_name": "Payne",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_crew_list(self):
        sample_crew()
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "Maksym",
            "last_name": "Protsak",
        }
        res = self.client.post(path=CREW_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        Crew.objects.create(first_name="John", last_name="Doe")
        payload = {
            "first_name": "John",
            "last_name": "Doe",
        }
        res = self.client.post(path=CREW_URL, data=payload)
        crew = Crew.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))
