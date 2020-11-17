from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('options', views.OptionViewSet)

app_name = 'menu'

urlpatterns = [
    path('', include(router.urls))
]
