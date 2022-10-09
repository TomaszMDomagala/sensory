from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensors/', include('sensors.urls')),
    path("users/", include("users.urls")),
    path('', RedirectView.as_view(url='sensors/')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)