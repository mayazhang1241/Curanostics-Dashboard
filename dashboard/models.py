from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')  # Links to Django's User model
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
# Signal to create/update UserProfile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
    
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
    date = models.DateField()
    steps = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='unique_user_date_step'
            )
        ]

class TriviaQuestion(models.Model):
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    wrong_answers = models.JSONField()  # Store a list of wrong answers

    def clean(self):
        if not isinstance(self.wrong_answers, list):
            raise ValidationError("Wrong answers must be a list of strings.")

    def __str__(self):
        return self.question

class UserTriviaProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE)
    answered_correctly = models.BooleanField(default=False)

class HydrationLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    water_intake = models.FloatField(default=0.0)  # Amount in oz.
    goal = models.FloatField(default=64.0)  # Default goal in liters (adjustable by the user)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.date}: {self.water_intake}L"

class ExerciseLog(models.Model):
    EXERCISE_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Yoga', 'Yoga'),
        ('Swimming', 'Swimming'),
        ('Weightlifting', 'Weightlifting'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    exercise_type = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.exercise_type} on {self.date}"

class ClinicalVisit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_type = models.CharField(max_length=100, choices=[
        ('upcoming', 'Upcoming'),
        ('recent', 'Recent'),
        ('previous', 'Previous')
    ])

    class Meta:
        ordering = ['-visit_date']

class PassportCategory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed')
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_case_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True, null=True)

    # Add relationships to other models
    allergies = models.ManyToManyField(Allergy, blank=True)
    immunizations = models.ManyToManyField(Immunization, blank=True)
    medications = models.ManyToManyField(Medication, blank=True)
    doctors = models.ManyToManyField(Doctor, blank=True)

    class Meta:
        ordering = ['category_name']

    def __str__(self):
        return f"{self.user.user.username} - {self.category_name}"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username}: {self.message[:50]}"