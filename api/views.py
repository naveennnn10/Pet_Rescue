from django.shortcuts import render

# Create your views here.

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
class HelloAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Pet Rescue API is up!"})

from rest_framework import viewsets, permissions
from .models import Pet
from .serializers import PetSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # attach the logged-in user as creator
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

# api/views.py
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Pet
from .serializers import PetSerializer

class PetCreateAPIView(generics.CreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]   # change to AllowAny for testing (not recommended)
    parser_classes = [JSONParser, MultiPartParser, FormParser]      # handle file uploads

    def perform_create(self, serializer):
        serializer.save()
