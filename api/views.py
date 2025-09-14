from django.shortcuts import render

# Create your views here.

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class HelloAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Pet Rescue API is up!"})
