from rest_framework import serializers
from .models import UserProfile, HydrationLog, ExerciseLog, TriviaQuestion, PassportCategory, Allergy, Immunization, Medication, Doctor, ChatMessage

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class HydrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydrationLog
        fields = '__all__'

class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

class TriviaQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriviaQuestion
        fields = '__all__'

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