from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile, HydrationLog, ExerciseLog, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, HydrationLogSerializer, ExerciseLogSerializer, TriviaQuestionSerializer, PassportCategorySerializer, AllergySerializer, ImmunizationSerializer, MedicationSerializer, DoctorSerializer, ChatMessageSerializer

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Health Dashboard!")

class UserProfileView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
class HydrationLogAPIView(APIView):
    def get(self, request):
        logs = HydrationLog.objects.all()
        serializer = HydrationLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = HydrationLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExerciseLogAPIView(APIView):
    def get(self, request):
        logs = ExerciseLog.objects.all()
        serializer = ExerciseLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExerciseLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TriviaQuestionAPIView(APIView):
    def get(self, request):
        questions = TriviaQuestion.objects.all()
        serializer = TriviaQuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
class PassportCategoryAPIView(APIView):
    def get(self, request):
        categories = PassportCategory.objects.all()
        serializer = PassportCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PassportCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllergyAPIView(APIView):
    def get(self, request):
        allergies = Allergy.objects.filter(user=request.user.userprofile)
        serializer = AllergySerializer(allergies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AllergySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class ImmunizationAPIView(APIView):
    def get(self, request):
        immunizations = Immunization.objects.filter(user=request.user.userprofile)
        serializer = ImmunizationSerializer(immunizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImmunizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class MedicationAPIView(APIView):
    def get(self, request):
        medications = Medication.objects.filter(user=request.user.userprofile)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class DoctorAPIView(APIView):
    def get(self, request):
        doctors = Doctor.objects.filter(user=request.user.userprofile)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class HealthPassportAPIView(APIView):
    def get(self, request):
        allergies = Allergy.objects.filter(user=request.user.userprofile)
        immunizations = Immunization.objects.filter(user=request.user.userprofile)
        medications = Medication.objects.filter(user=request.user.userprofile)
        doctors = Doctor.objects.filter(user=request.user.userprofile)

        data = {
            "allergies": AllergySerializer(allergies, many=True).data,
            "immunizations": ImmunizationSerializer(immunizations, many=True).data,
            "medications": MedicationSerializer(medications, many=True).data,
            "doctors": DoctorSerializer(doctors, many=True).data,
        }
        return Response(data)
    
class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = request.user.userprofile
            serializer.save(user=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)