from django.shortcuts import render

# Create your views here.

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import viewsets, permissions
from .models import Pet
from .serializers import PetSerializer
from rest_framework import generics, permissions
class HelloAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Pet Rescue API is up!"})

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

class PetCreateAPIView(generics.CreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]   # change to AllowAny for testing (not recommended)
    parser_classes = [JSONParser, MultiPartParser, FormParser]      # handle file uploads

    def perform_create(self, serializer):
        serializer.save()


class PetListAPIView(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]   # public read

    def get_queryset(self):
        qs = Pet.objects.all().order_by('-created_date')
        # simple filtering via query params
        pet_type = self.request.query_params.get('pet_type')  # expects pet_type id
        city = self.request.query_params.get('city')
        state = self.request.query_params.get('state')
        vaccinated = self.request.query_params.get('is_vaccinated')  # 'true' or 'false'
        diseased = self.request.query_params.get('is_diseased')

        if pet_type:
            qs = qs.filter(pet_type__id=pet_type)
        if city:
            qs = qs.filter(city__icontains=city)
        if state:
            qs = qs.filter(state__icontains=state)
        if vaccinated is not None:
            if vaccinated.lower() in ('true', '1', 'yes'):
                qs = qs.filter(is_vaccinated=True)
            elif vaccinated.lower() in ('false', '0', 'no'):
                qs = qs.filter(is_vaccinated=False)
        if diseased is not None:
            if diseased.lower() in ('true', '1', 'yes'):
                qs = qs.filter(is_diseased=True)
            elif diseased.lower() in ('false', '0', 'no'):
                qs = qs.filter(is_diseased=False)

        return qs

class PetRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]
