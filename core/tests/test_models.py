from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

import datetime


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@cornershop.cl"
        password = "password123"
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "teSt@cornerShOp.cl"
        user = get_user_model().objects.create_user(email, "password123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creation user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "password123")

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
