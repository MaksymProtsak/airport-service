from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timezone

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Route, Flight
from airport.serializers import FlightSerializer
from airport.tests.test_airplane_api import sample_airplane
from airport.tests.test_route_api import sample_route

FLIGHT_URL = reverse("airport:flight-list")


def sample_flight() -> Flight:
    route = sample_route()
    airplane = sample_airplane()
    flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=datetime(2024, 6, 1, 13, 15),
        arrival_time=datetime(2024, 6, 1, 14, 30)
    )
    return flight


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_flight_list(self):
        sample_flight()
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_flight_forbidden(self):
        route = sample_route()
        airplane = sample_airplane()
        departure_time = datetime(2024, 6, 1, 13, 15, ),
        arrival_time = datetime(2024, 6, 1, 14, 30)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": arrival_time
        }
        res = self.client.post(path=FLIGHT_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        departure_time = datetime(
            2024,
            6,
            1,
            13,
            15,
            tzinfo=timezone.utc
        )
        arrival_time = datetime(
            2024,
            6,
            1,
            14,
            30,
            tzinfo=timezone.utc
        )

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        }
        res = self.client.post(path=FLIGHT_URL, data=payload)
        flight = Flight.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(flight.route.id, payload["route"])
        self.assertEqual(flight.airplane.id, payload["airplane"])
        self.assertEqual(flight.departure_time, payload["departure_time"])
        self.assertEqual(flight.arrival_time, payload["arrival_time"])

    def test_create_flight_already_exist(self):
        s_flight = sample_flight()
        payload = {
            "route": s_flight.route.id,
            "airplane": s_flight.airplane.id,
            "departure_time": s_flight.departure_time,
            "arrival_time": s_flight.arrival_time,
        }
        res = self.client.post(path=FLIGHT_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["flight_exist"][0].title().lower(),
            f"Flight with route '{Route.objects.get(id=payload["route"])}'"
            f"already exist.".lower()
        )
        self.assertEqual(
            res.data["flight_exist"][0].code,
            "invalid"
        )

    def test_create_flight_with_same_departure_and_arrival_time(self):
        s_flight = sample_flight()
        payload = {
            "route": s_flight.route.id,
            "airplane": s_flight.airplane.id,
            "departure_time": s_flight.departure_time,
            "arrival_time": s_flight.departure_time,
        }
        res = self.client.post(path=FLIGHT_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["departure_time"][0].title().lower(),
            "The departure time and arrival time cannot be same.".lower()
        )
        self.assertEqual(
            res.data["departure_time"][0].code,
            "invalid"
        )
