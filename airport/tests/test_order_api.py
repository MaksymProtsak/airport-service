from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from airport.models import Order
from airport.serializers import OrderSerializer
from airport.tests.test_flight_api import sample_flight

ORDER_URL = reverse("airport:order-list")


def sample_order(**params) -> Order:
    defaults = {
        "user": params["user"],
    }
    defaults.update(params)
    return Order.objects.create(**defaults)


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_order_list(self):
        sample_order(user=self.user)
        sample_order(
            user=get_user_model().objects.create_user(
                email="admin@admin.com",
                password="TestPassword123",
            )
        )
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_order_forbidden(self):
        payload = {
            "user": self.user,
        }
        res = self.client.post(path=ORDER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_order_bad_request(self):
        sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": 1
                }
            ]
        }
        res = self.client.post(path=ORDER_URL, data=payload,)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(res.data.keys()), ["tickets"])

    def test_create_order(self):
        sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": 1
                }
            ]
        }
        res = self.client.post(path=ORDER_URL, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
