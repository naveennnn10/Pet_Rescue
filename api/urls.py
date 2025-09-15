# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HelloAPI, PetViewSet, PetCreateAPIView, PetListAPIView, PetRetrieveAPIView

# DRF Router
router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    path('', HelloAPI.as_view(), name='api-root'),
    path('pets/create/', PetCreateAPIView.as_view(), name='pet-create'),
    path('', include(router.urls)),   # all viewset routes
    path('pets/', PetListAPIView.as_view(), name='pet-list'),
    path('pets/<int:pk>/', PetRetrieveAPIView.as_view(), name='pet-detail'),
]


