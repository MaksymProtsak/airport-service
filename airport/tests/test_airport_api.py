from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Airport
from airport.serializers import AirportSerializer

AIRPORT_URL = reverse("airport:airport-list")


def sample_airport(**params) -> Airport:
    defaults = {
        "name": "Dallas Fort Worth International Airport",
        "closest_big_city": "Dallas",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airport_list(self):
        sample_airport()
        sample_airport(
            name="Boryspil International Airport",
            closest_big_city="Kyiv"
        )
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_crew_forbidden(self):
        payload = {
            "name": "Boryspil International Airport",
            "closest_big_city": "Kyiv",
        }
        res = self.client.post(path=AIRPORT_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        Airport.objects.create(
            name="Boryspil International Airport",
            closest_big_city="Kyiv"
        )
        payload = {
            "name": "Boryspil International Airport",
            "closest_big_city": "Kyiv",
        }
        res = self.client.post(path=AIRPORT_URL, data=payload)
        airport = Airport.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))
