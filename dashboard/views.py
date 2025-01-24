import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile, HydrationLog, ExerciseLog, StepTracker, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage, ClinicalVisit
import logging
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, HydrationLogSerializer, ExerciseLogSerializer, StepTrackerSerializer, TriviaQuestionSerializer, PassportCategorySerializer, AllergySerializer, ImmunizationSerializer, MedicationSerializer, DoctorSerializer, ChatMessageSerializer, ClinicalVisitSerializer

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Health Dashboard!")

class UserProfileView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
class HydrationLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    
class StepTrackerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        steps = StepTracker.objects.filter(user=request.user.userprofile).order_by('-date')
        serializer = StepTrackerSerializer(steps, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StepTrackerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
logger = logging.getLogger(__name__)

class TriviaQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Use OpenFDA API to fetch trivia questions dynamically
        external_api_url = "https://api.fda.gov/drug/event.json?search=serious:1&limit=20"

        try:
            response = requests.get(external_api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                # Retrieve the user's session data
                session = request.session
                answered_questions = session.get("answered_questions", [])

                # Collect all unique reactions
                all_reactions = [
                    reaction.get("reactionmeddrapt", "Unknown")
                    for item in results
                    for reaction in item.get("patient", {}).get("reaction", [])
                ]

                # Define diverse question templates
                question_templates = [
                    "What is a reported reaction to a drug?",
                    "Which of these reactions has been reported in adverse events?",
                    "Identify the correct reaction from the options below.",
                    "What is one possible adverse reaction from the FDA database?",
                    "Can you spot the reported reaction?",
                    "Which reaction is listed in the database?",
                    "A patient reported which of the following reactions?",
                    "Select the correct adverse event from these options.",
                    "Which of the following reactions has been marked as serious?",
                    "Identify a reaction associated with adverse drug events."
                ]

                questions = []

                for item in results:
                    reactions = item.get("patient", {}).get("reaction", [])
                    if reactions:
                        correct_answer = reactions[0].get("reactionmeddrapt", "Unknown")

                        # Skip already answered questions
                        if correct_answer in answered_questions:
                            continue

                        wrong_answers = list(set(all_reactions) - {correct_answer})[:3]

                        # Randomly select a question template
                        question_text = random.choice(question_templates)

                        question = {
                            "question": question_text,
                            "correct_answer": correct_answer,
                            "wrong_answers": wrong_answers if len(wrong_answers) >= 3 else ["Unknown", "Other", "None"]
                        }
                        questions.append(question)

                # If no new questions available, reset the session
                if not questions:
                    session["unanswered_questions"] = []
                    session.save()
                    return Response({"message": "All questions answered. Restarting trivia."}, status=status.HTTP_200_OK)

                # Select one question randomly and update the session
                selected_question = random.choice(questions)
                answered_questions.append(selected_question["correct_answer"])
                session["answered_questions"] = answered_questions
                session.save()

                return Response(selected_question, status=status.HTTP_200_OK)
                
            else:
                return Response({"error": "Failed to fetch trivia questions"}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    
class ClinicalVisitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visits = ClinicalVisit.objects.filter(user=request.user.userprofile).order_by('-visit_date')
        serializer = ClinicalVisitSerializer(visits, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ClinicalVisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)