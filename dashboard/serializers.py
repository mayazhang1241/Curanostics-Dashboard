from rest_framework import serializers
from .models import UserProfile, HydrationLog, ExerciseLog, StepTracker, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage, ClinicalVisit

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class HydrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydrationLog
        fields = ['id', 'user', 'water_intake', 'goal', 'date']
        read_only_fields = ['id', 'user', 'date']

class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = ['id', 'user', 'exercise_type', 'duration_minutes', 'calories_burned', 'date']
        read_only_fields = ['id', 'user', 'date']

class StepTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepTracker
        fields = ['id', 'user', 'steps', 'date']
        read_only_fields = ['id', 'user', 'date']

class TriviaQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriviaQuestion
        fields = ['id', 'question', 'correct_answer', 'wrong_answers']
        read_only_fields = ['id']

class PassportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportCategory
        fields = '__all__'

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

class ImmunizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunization
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

class ClinicalVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalVisit
        fields = ['id', 'user', 'visit_type', 'visit_date']
        read_only_fields = ['id', 'user']