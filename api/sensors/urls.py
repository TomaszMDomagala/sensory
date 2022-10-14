from django.urls import path, include
from .views import (
    SensorsListApiView,
)

urlpatterns = [
    path('api', SensorsListApiView.as_view()),
]