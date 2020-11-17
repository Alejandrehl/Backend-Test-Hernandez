from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):
    """User Manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=email.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Option(models.Model):
    """Option to be used for a menu"""
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Menu(models.Model):
    """Menu object"""
    name = models.CharField(default="Today's menu", max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order created by an user"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )
    observation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
