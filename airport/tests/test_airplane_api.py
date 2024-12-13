from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneSerializer

AIRPLANE_URL = reverse("airport:airplane-list")


def sample_airplane(**params) -> Airplane:
    defaults = {
        "name": "747-400",
        "rows": 50,
        "seats_in_row": 8,
        "airplane_type": AirplaneType.objects.create(name="Passenger")

    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airplane_list(self):
        sample_airplane()
        airplanes = Airplane.objects.all()
        serializer = AirplaneSerializer(airplanes, many=True)
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        AirplaneType.objects.create(name="Passenger")
        payload = {
            "name": "Boeing 737",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": 1,
        }
        res = self.client.post(path=AIRPLANE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = AirplaneType.objects.create(name="Passenger")
        Airplane.objects.create(
            name="Boeing 737",
            rows=30,
            seats_in_row=6,
            airplane_type=airplane_type,
        )
        payload = {
            "name": "Boeing 737",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": 1,
        }
        res = self.client.post(path=AIRPLANE_URL, data=payload)
        airplane = Airplane.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(airplane.name, payload["name"])
        self.assertEqual(airplane.rows, payload["rows"])
        self.assertEqual(airplane.seats_in_row, payload["seats_in_row"])
        self.assertEqual(airplane.airplane_type.id, payload["airplane_type"])
