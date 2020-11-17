from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Option, Menu

from menu.serializers import OptionSerializer

import datetime

OPTIONS_URL = reverse('recipe:option-list')


class PublicOptionsApiTests(TestCase):
    """Test the publicity available options API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving options"""
        res = self.client.get(OPTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOptionsApiTests(TestCase):
    """Test the authorized options API"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="alejandrehl@icloud.com",
            password="password123",
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_options(self):
        """Test retrieving options"""
        Option.objects.create(description='Corn pie, Salad and Dessert')
        Option.objects.create(
            description='Chicken Nugget Rice, Salad and Dessert')

        res = self.client.get(OPTIONS_URL)

        options = Option.objects.all().order_by('-description')
        serializer = OptionSerializer(options, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_options_limited_to_staff_user(self):
        """Test the options returned only for staff users"""
        option = Option.objects.create(
            description='Chicken Nugget Rice, Salad and Dessert')
        Option.objects.create(description='Corn pie, Salad and Dessert')

        res = self.client.get(OPTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['description'], option.description)

    def test_create_option_successful(self):
        """Test creating a new option"""
        payload = {'description': 'Rice with hamburger, Salad and Dessert'}
        self.client.post(OPTIONS_URL, payload)

        exists = Option.objects.filter(
            name=payload['description']
        ).exists()

        self.assertTrue(exists)

    def test_create_option_invalid(self):
        """Test creating a new option with invalid payload"""
        payload = {'description': ''}
        res = self.client.post(OPTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_options_assigned_to_menus(self):
        """Test filtering options by those assigned to menus"""
        option1 = Option.objects.create(
            description='Premium chicken Salad and Dessert.')
        option2 = Option.objects.create(
            description='Chicken Nugget Rice, Salad and Dessert')
        menu = Menu.objects.create(
            date=datetime.date.fromisoformat("2020-12-01")
        )
        menu.options.add(option1)

        res = self.client.get(OPTIONS_URL, {'assigned_only': 1})

        serializer1 = OptionSerializer(option1)
        serializer2 = OptionSerializer(option2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_options_assigned_unique(self):
        """Test filtering options by assigned returns unique items"""
        option = Option.objects.create(
            description='Chicken Nugget Rice, Salad and Dessert')
        Option.objects.create(description='Premium chicken Salad and Dessert')
        menu1 = Menu.objects.create(
            date=datetime.date.fromisoformat("2020-12-01")
        )
        menu1.options.add(option)
        menu2 = Menu.objects.create(
            date=datetime.date.fromisoformat("2020-12-05")
        )
        menu2.options.add(option)

        res = self.client.get(OPTIONS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
