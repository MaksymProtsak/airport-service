from typing import Tuple

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Route, Airport
from airport.serializers import RouteSerializer

ROUTE_URL = reverse("airport:route-list")


def sample_airports() -> Tuple:
    source = Airport.objects.create(
        name="IEV",
        closest_big_city="Kyiv"
    )
    destination = Airport.objects.create(
        name="NLV",
        closest_big_city="Mykolaiv",
    )
    return source, destination


def sample_route(**params) -> Route:
    source, destination = sample_airports()
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 400,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_route_list(self):
        sample_route()
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airplane_forbidden(self):
        source = Airport.objects.create(
            name="IEV",
            closest_big_city="Kyiv"
        )
        destination = Airport.objects.create(
            name="NLV",
            closest_big_city="Mykolaiv",
        )
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 400,
        }
        res = self.client.post(path=ROUTE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        source, destination = sample_airports()
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 400,
        }
        res = self.client.post(path=ROUTE_URL, data=payload)
        route = Route.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(route.source.id, payload["source"])
        self.assertEqual(route.destination.id, payload["destination"])
        self.assertEqual(route.distance, payload["distance"])

    def test_create_route_already_exist(self):
        source, destination = sample_airports()
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 400,
        }
        res = self.client.post(path=ROUTE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(path=ROUTE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["non_field_errors"][0].title(),
            "The Fields Source, Destination Must Make A Unique Set."
        )
        self.assertEqual(
            res.data["non_field_errors"][0].code,
            "unique"
        )

    def test_create_route_destination_adn_source_equal(self):
        source, destination = sample_airports()
        payload = {
                    "source": source.id,
                    "destination": source.id,
                    "distance": 400,
        }
        res = self.client.post(path=ROUTE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["non_field_errors"][0].title(),
            "The destination and source are equal."
        )
        self.assertEqual(
            res.data["non_field_errors"][0].code,
            "invalid"
        )
