# Requerimientos
# Solo Nora puede crear, ediatar y eliminar menus (STAFF USER)
# Para crear un menu primero debe agregar opciones
# Un Menu se debe componen de hasta 4 opciones diarias
# Solo puede haber un menu diario
# Todos los usuarios o no usuarios pueden ver el menú del día

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Menu, Option

from menu.serializers import MenuSerializer

import datetime

MENUS_URL = reverse('menu:menu-list')


class PublicMenusApiTests(TestCase):
    """Test the publicity available options API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_daily_menu(self):
        """Test retrieving daily menus"""
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
