from django.urls import path, include
from .views import (
    SensorsListApiView,
    SensorsView,
)

urlpatterns = [
    path('api', SensorsListApiView.as_view()),
    path('', SensorsView.as_view(), name="main"),
]