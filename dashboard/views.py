from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile
from rest_framework import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Health Dashboard!")

class UserProfileView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)