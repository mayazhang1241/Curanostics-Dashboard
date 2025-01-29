from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, HydrationLog, ExerciseLog, StepTracker, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage, ClinicalVisit

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    birth_date = serializers.DateField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 
                 'first_name', 'last_name', 'birth_date')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        birth_date = validated_data.pop('birth_date')
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user.userprofile.birth_date = birth_date
        user.userprofile.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 
                 'email', 'birth_date', 'profile_picture')
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

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

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class ImmunizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunization
        fields = ['id', 'name', 'date_received']
        read_only_fields = ['id']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'dosage', 'instructions']
        read_only_fields = ['id']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'contact_info']
        read_only_fields = ['id']

class PassportCategorySerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)
    immunizations = ImmunizationSerializer(many=True, read_only=True)
    medications = MedicationSerializer(many=True, read_only=True)
    doctors = DoctorSerializer(many=True, read_only=True)

    class Meta:
        model = PassportCategory
        fields = ['id', 'category_name', 'status', 'last_case_date', 
                 'details', 'allergies', 'immunizations', 
                 'medications', 'doctors']
        read_only_fields = ['id']

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