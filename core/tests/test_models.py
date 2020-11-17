from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_option_str(self):
        """Test the option string representation"""
        option = models.Option.objects.create(
            name='Corn pie, Salad and Dessert'
        )

        self.assertEqual(str(option), option.description)

    def test_menu_str(self):
        """Test the ingrediente string representation"""
        menu = models.Menu.objects.create(
            name='Vegan Menu'
        )

        self.assertEqual(str(menu), menu.name)
