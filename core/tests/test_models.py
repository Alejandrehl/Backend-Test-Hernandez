from django.db.models.fields import DateField
from django.test import TestCase

from core import models

import datetime


class ModelTests(TestCase):
    """Test models"""

    def test_option_str(self):
        """Test the option string representation"""
        option = models.Option.objects.create(
            description='Corn pie, Salad and Dessert'
        )

        self.assertEqual(str(option), option.description)

    def test_menu_str(self):
        """Test the ingrediente string representation"""
        menu = models.Menu.objects.create(
            name='Vegan Menu',
            date=datetime.date.fromisoformat("2020-11-16")
        )

        self.assertEqual(str(menu), menu.name)
