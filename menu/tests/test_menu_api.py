from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Menu, Option, Order

from menu.serializers import MenuDetailSerializer, MenuSerializer

import datetime

MENUS_URL = reverse('menu:menu-list')


def sample_menu(**params):
    """Create and return a sample menu"""
    option1 = Option.objects.create(
        description='Corn pie, Salad and Dessert')
    option2 = Option.objects.create(
        description='Chicken Nugget Rice, Salad and Dessert')

    defaults = {
        'name': "Today's Menu",
        'date': datetime.date.today(),
    }
    defaults.update(params)

    menu = Menu.objects.create(**defaults)
    menu.options.add(option1)
    menu.options.add(option2)
    return menu


def sample_option(description='Chicken Nugget Rice, Salad and Dessert'):
    """Create and return a sample option"""
    return Option.objects.create(description=description)


def sample_order(user, menu):
    """Create and return a sample order"""
    return Order.objects.create(user, menu, observation="No tomatoes in the salad")


def detail_url(menu_id):
    """Return menu detail URL"""
    return reverse('menu:menu-detail', args=[menu_id])


class PublicMenuApiTests(TestCase):
    """Test the publicity available options API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_menus(self):
        """Test retrieving menus"""
        option1 = Option.objects.create(
            description='Corn pie, Salad and Dessert')
        option2 = Option.objects.create(
            description='Chicken Nugget Rice, Salad and Dessert')

        menu = Menu.objects.create(date=datetime.date.today())
        menu.options.add(option1)
        menu.options.add(option2)

        res = self.client.get(MENUS_URL)

        menus = Menu.objects.all().order_by('-date')
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_menu_detail(self):
        """Test viewing a menu detail"""
        menu = sample_menu()
        menu.options.add(sample_option())
        menu.options.add(sample_option())

        url = detail_url(menu.id)
        res = self.client.get(url)

        serializer = MenuDetailSerializer(menu)
        self.assertEqual(res.data, serializer.data)


class PrivateMenuApiTest(TestCase):
    """Test authenticated menu API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'nora@cornershop.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_create_basic_menu(self):
        """Test creating menu without options"""
        payload = {
            'name': "Today's Menu",
            'date': datetime.date.today(),
        }
        res = self.client.post(MENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu_with_options(self):
        """Test creating a menu with options"""
        option1 = sample_option()
        option2 = sample_option()
        payload = {
            'name': "Today's Menu",
            'date': datetime.date.today(),
            'options': [option1.id, option2.id]
        }

        res = self.client.post(MENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        menu = Menu.objects.get(id=res.data['id'])
        options = menu.options.all()
        self.assertEqual(options.count(), 2)
        self.assertIn(option1, options)
        self.assertIn(option2, options)

    def test_partial_update_menu(self):
        """Test updating a menu with patch"""
        menu = sample_menu()
        menu.options.add(sample_option())
        new_option = sample_option()

        payload = {'name': 'Vegan Menu', 'options': [new_option.id]}
        url = detail_url(menu.id)
        self.client.patch(url, payload)

        menu.refresh_from_db()
        self.assertEqual(menu.name, payload['name'])
        options = menu.options.all()
        self.assertEqual(len(options), 1)
        self.assertIn(new_option, options)

    def test_full_update_menu(self):
        """Test updating a menu with put"""
        menu = sample_menu()
        menu.options.add(sample_option())

        payload = {
            'name': 'Chilean Menu',
            'date': datetime.date.today(),
            'options': []
        }
        url = detail_url(menu.id)
        self.client.put(url, payload)

        menu.refresh_from_db()
        self.assertEqual(menu.name, payload['name'])
        self.assertEqual(menu.date, payload['date'])
        options = menu.options.all()
        self.assertEqual(len(options), 0)
