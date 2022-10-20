from django.urls import path, include
from .views import (
    SensorsListApiView,
    SensorsView,
    ChartView
)


urlpatterns = [
    path('api', SensorsListApiView.as_view()),
    path('', SensorsView.as_view(), name="main"),
    path('charts', ChartView.as_view(), name='charts')
]