from django.urls import path
from . import views
from .views import UserProfileView, HydrationLogAPIView, ExerciseLogAPIView, TriviaQuestionAPIView, PassportCategoryAPIView, AllergyAPIView, ImmunizationAPIView, MedicationAPIView, DoctorAPIView, ChatAPIView

urlpatterns = [
    path('', views.home, name='home'),  # Route for the homepage

    # User Profile
    path('api/user-profiles/', UserProfileView.as_view(), name='user-profiles'),

    # Logs
    path('api/hydration-logs/', HydrationLogAPIView.as_view(), name='hydration-logs'),
    path('api/exercise-logs/', ExerciseLogAPIView.as_view(), name='exercise-logs'),

    # Trivia
    path('api/trivia-questions/', TriviaQuestionAPIView.as_view(), name='trivia-questions'),

    # Passport Data
    path('api/passport-categories/', PassportCategoryAPIView.as_view(), name='passport-categories'),

    # Health Categories
    path('api/allergies/', AllergyAPIView.as_view(), name='allergies'),
    path('api/immunizations/', ImmunizationAPIView.as_view(), name='immunizations'),
    path('api/medications/', MedicationAPIView.as_view(), name='medications'),
    path('api/doctors/', DoctorAPIView.as_view(), name='doctors'),

    # ChatBot
    path('chat/', ChatAPIView.as_view(), name='chat')
]