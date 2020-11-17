from django.urls import path, include

urlpatterns = [
    path('api/user/', include('user.urls')),
    path('api/menu/', include('menu.urls')),
]
