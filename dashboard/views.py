import random
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import UserProfile, HydrationLog, ExerciseLog, StepTracker, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage, ClinicalVisit
import logging
import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer, 
                          HydrationLogSerializer, ExerciseLogSerializer, StepTrackerSerializer, TriviaQuestionSerializer, 
                          PassportCategorySerializer, AllergySerializer, ImmunizationSerializer, MedicationSerializer, 
                          DoctorSerializer, ChatMessageSerializer, ClinicalVisitSerializer)

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Health Dashboard!")

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                
                # Add debug prints
                print(f"User created: {user.username}")
                print(f"Token created: {token.key}")
                
                return Response({
                    'token': token.key,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in registration: {str(e)}")  # Debug print
            return Response(
                {'error': 'Registration failed', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user.userprofile).data
            })
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = request.user
            profile = user.userprofile
            
            # Print debug information
            print(f"Received data: {request.data}")
            
            serializer = UserProfileSerializer(
                profile,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                print(f"Valid data: {serializer.validated_data}")
                
                # Update User model fields
                if 'user' in serializer.validated_data:
                    user_data = serializer.validated_data.pop('user')
                    for attr, value in user_data.items():
                        setattr(user, attr, value)
                    user.save()
                
                # Update UserProfile fields
                serializer.save()
                
                return Response(serializer.data)
            
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return Response(
                {'error': f'Profile update failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data['old_password']):
                if serializer.data['new_password'] == serializer.data['confirm_password']:
                    user.set_password(serializer.data['new_password'])
                    user.save()
                    return Response({'message': 'Password updated successfully'})
                return Response(
                    {'error': 'New passwords don\'t match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'profile_picture' not in request.FILES:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        profile = request.user.userprofile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        return Response({
            'message': 'Profile picture updated successfully',
            'url': profile.profile_picture.url
        })
    
class HydrationLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            hydration_logs = HydrationLog.objects.filter(
                user=request.user.userprofile
            ).order_by('-date')

            print(f"Found {hydration_logs.count()} logs")

            serializer = HydrationLogSerializer(hydration_logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error in get: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            print(f"Received data: {request.data}")

            serializer = HydrationLogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user.userprofile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            print(f"Validation errors: {serializer.errors}")  # Debug print
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in post: {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ExerciseLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            exercise_logs = ExerciseLog.objects.filter(
                user=request.user.userprofile
            ).order_by('-date')

            print(f"Found {exercise_logs.count()} exercise logs")

            serializer = ExerciseLogSerializer(exercise_logs, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            print(f"Error in get: {str(e)}")  # Debug print
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post(self, request):
        try:
            print(f"Received exercise data: {request.data}")

            serializer = ExerciseLogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user.userprofile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            print(f"Validation errors: {serializer.errors}")  # Debug print
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"Error in post: {str(e)}")  # Debug print
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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
        categories = PassportCategory.objects.filter(
            user=request.user.userprofile
        ).prefetch_related(
            'allergies', 'immunizations', 'medications', 'doctors'
        )
        serializer = PassportCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            data = request.data.copy()
            # Handle related items
            allergies = data.pop('allergies', [])
            immunizations = data.pop('immunizations', [])
            medications = data.pop('medications', [])
            doctors = data.pop('doctors', [])

            serializer = PassportCategorySerializer(data=data)
            if serializer.is_valid():
                category = serializer.save(user=request.user.userprofile)
                
                # Add relationships
                if allergies:
                    category.allergies.set(allergies)
                if immunizations:
                    category.immunizations.set(immunizations)
                if medications:
                    category.medications.set(medications)
                if doctors:
                    category.doctors.set(doctors)
                
                # Re-serialize with related data
                return Response(
                    PassportCategorySerializer(category).data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class PassportCategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = PassportCategory.objects.prefetch_related(
                'allergies', 'immunizations', 'medications', 'doctors'
            ).get(user=request.user.userprofile, pk=pk)
            serializer = PassportCategorySerializer(category)
            return Response(serializer.data)
        except PassportCategory.DoesNotExist:
            return Response(
                {"error": "Category not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
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
        try:
            visits = ClinicalVisit.objects.filter(user=request.user.userprofile).order_by('-visit_date')

            print(f"Found {visits.count()} visits")

            if not visits.exists():
                return Response({"message": "No clinical visits recorded."}, status=status.HTTP_404_NOT_FOUND)
        
            today = timezone.now().date()

            # Find the upcoming, last, and previous visits
            upcoming = visits.filter(visit_date__gte=today).first()
            past_visits = visits.filter(visit_date__lt=today)

            print(f"Upcoming visits: {upcoming}")  # Debug print
            print(f"Past visits count: {past_visits.count()}")  # Debug print

            last = past_visits.last() if past_visits.exists() else None
            previous = past_visits[len(past_visits) - 2] if past_visits.count() > 1 else None

            response_data = {
                "upcoming": {
                    "date": upcoming.visit_date,
                    "visit_type": upcoming.visit_type
                } if upcoming else None,
                "last": {
                    "date": last.visit_date,
                    "visit_type": last.visit_type
                } if last else None,
                "previous": {
                    "date": previous.visit_date,
                    "visit_type": previous.visit_type
                } if previous else None,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error in get: {str(e)}")  # Debug print
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            serializer = ClinicalVisitSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user.userprofile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in post: {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )