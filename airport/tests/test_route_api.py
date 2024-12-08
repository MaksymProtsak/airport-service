from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Route, Airport
from airport.serializers import RouteSerializer

ROUTE_URL = reverse("airport:route-list")


def sample_route(**params) -> Route:
    source = Airport.objects.create(
        name="IEV",
        closest_big_city="Kyiv"
    )
    destination = Airport.objects.create(
        name="NLV",
        closest_big_city="Mykolaiv",
    )
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

#     def test_create_airplane(self):
#         airplane_type = AirplaneType.objects.create(name="Passenger")
#         Airplane.objects.create(
#             name="Boeing 737",
#             rows=30,
#             seats_in_row=6,
#             airplane_type=airplane_type,
#         )
#         payload = {
#             "name": "Boeing 737",
#             "rows": 30,
#             "seats_in_row": 6,
#             "airplane_type": 1,
#         }
#         res = self.client.post(path=AIRPLANE_URL, data=payload)
#         airplane = Airplane.objects.get(id=res.data["id"])
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(airplane.name, payload["name"])
#         self.assertEqual(airplane.rows, payload["rows"])
#         self.assertEqual(airplane.seats_in_row, payload["seats_in_row"])
#         self.assertEqual(airplane.airplane_type.id, payload["airplane_type"])
