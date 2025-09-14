# api/urls.py
from django.urls import path
from .views import HelloAPI

urlpatterns = [
    path('', HelloAPI.as_view(), name='api-root'),
    # later you'll add paths or include routers here, e.g.
    # path('pets/', include('api.pets_urls')) or use a DRF router
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    path('', include(router.urls)),
]
