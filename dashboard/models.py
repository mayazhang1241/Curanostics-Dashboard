from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Links to Django's User model
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    steps_goal = models.IntegerField(default=10000)
    hydration_goal = models.IntegerField(default=64)

    def __str__(self):
        return self.user.username
    
class Allergy(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class Immunization(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_received = models.DateField()

class Medication(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)

class Doctor(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)
    contact_info = models.TextField()

# Gamification

class StepTracker(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)

class TriviaQuestion(models.Model):
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    wrong_answers = models.JSONField()  # Store a list of wrong answers

class UserTriviaProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE)
    answered_correctly = models.BooleanField(default=False)

class HydrationLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    water_intake = models.IntegerField(default=0)  # Amount in oz.

class ExerciseLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    exercise = models.CharField(max_length=255)

class ClinicalVisit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_type = models.CharField(max_length=100, choices=[
        ('upcoming', 'Upcoming'),
        ('recent', 'Recent'),
        ('previous', 'Previous')
    ])