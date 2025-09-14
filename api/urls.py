# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HelloAPI, PetViewSet, PetCreateAPIView

# DRF Router
router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    path('', HelloAPI.as_view(), name='api-root'),
    path('pets/', PetCreateAPIView.as_view(), name='pet-create'),
    path('', include(router.urls)),   # all viewset routes
]


