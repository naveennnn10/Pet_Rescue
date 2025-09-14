# api/urls.py
from django.urls import path
from .views import HelloAPI

urlpatterns = [
    path('', HelloAPI.as_view(), name='api-root'),
    # later you'll add paths or include routers here, e.g.
    # path('pets/', include('api.pets_urls')) or use a DRF router
]
