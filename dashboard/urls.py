from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import ProfileView, HydrationLogAPIView, ExerciseLogAPIView, TriviaQuestionAPIView, PassportCategoryAPIView, AllergyAPIView, ImmunizationAPIView, MedicationAPIView, DoctorAPIView, ChatAPIView, PassportCategoryDetailAPIView

urlpatterns = [
    path('', views.home, name='home'),  # Route for the homepage

    # User Profile
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/upload-picture/', views.ProfilePictureView.as_view(), name='upload-picture'),

    # Step Tracker
    path('api/steps/', views.StepTrackerAPIView.as_view(), name='step-tracker-api'),

    # Logs
    path('api/hydration-logs/', HydrationLogAPIView.as_view(), name='hydration-log-api'),
    path('api/exercise-logs/', ExerciseLogAPIView.as_view(), name='exercise-log-api'),

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
    path('chat/', ChatAPIView.as_view(), name='chat'),

    # Clinical Visits
    path('clinical-visits/', views.ClinicalVisitAPIView.as_view(), name='clinical-visits-api'),

    # Detailed Passport
    path('api/passport-categories/<int:pk>/', 
     PassportCategoryDetailAPIView.as_view(), 
     name='passport-category-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)