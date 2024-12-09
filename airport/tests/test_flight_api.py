from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Route, Flight
from airport.serializers import FlightSerializer
from airport.tests.test_airplane_api import sample_airplane
from airport.tests.test_route_api import sample_airports, sample_route

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
        departure_time = datetime(2024, 6, 1, 13, 15),
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
        departure_time = datetime(2024, 6, 1, 13, 15),
        arrival_time = datetime(2024, 6, 1, 14, 30)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": arrival_time
        }
        res = self.client.post(path=FLIGHT_URL, data=payload)
        flight = Flight.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(flight.route.id, payload["route"])
        self.assertEqual(flight.airplane.id, payload["airplane"])
        self.assertEqual(flight.departure_time, payload["departure_time"])
        self.assertEqual(flight.arrival_time, payload["arrival_time"])

    # def test_create_route_already_exist(self):
    #     source, destination = sample_airports()
    #     payload = {
    #         "source": source.id,
    #         "destination": destination.id,
    #         "distance": 400,
    #     }
    #     res = self.client.post(path=ROUTE_URL, data=payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     res = self.client.post(path=ROUTE_URL, data=payload)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data["non_field_errors"][0].title(),
    #         "The Fields Source, Destination Must Make A Unique Set."
    #     )
    #     self.assertEqual(
    #         res.data["non_field_errors"][0].code,
    #         "unique"
    #     )
    #
    # def test_create_route_destination_adn_source_equal(self):
    #     source, destination = sample_airports()
    #     payload = {
    #                 "source": source.id,
    #                 "destination": source.id,
    #                 "distance": 400,
    #     }
    #     res = self.client.post(path=ROUTE_URL, data=payload)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data["non_field_errors"][0].title(),
    #         "The destination and source are equal."
    #     )
    #     self.assertEqual(
    #         res.data["non_field_errors"][0].code,
    #         "invalid"
    #     )
