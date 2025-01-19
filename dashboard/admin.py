from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Allergy)
admin.site.register(Immunization)
admin.site.register(Medication)
admin.site.register(Doctor)
admin.site.register(StepTracker)
admin.site.register(TriviaQuestion)
admin.site.register(UserTriviaProgress)
admin.site.register(HydrationLog)
admin.site.register(ExerciseLog)
admin.site.register(ClinicalVisit)