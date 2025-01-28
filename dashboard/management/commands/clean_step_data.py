from django.core.management.base import BaseCommand
from dashboard.models import StepTracker
from django.db.models import Max

class Command(BaseCommand):
    help = 'Clean up duplicate step tracker entries'

    def handle(self, *args, **kwargs):
        # Get all unique user-date combinations
        duplicates = (
            StepTracker.objects
            .values('user', 'date')
            .annotate(max_id=Max('id'))
            .filter(user__isnull=False)
        )

        # Keep only the latest entry for each user-date combination
        for dup in duplicates:
            StepTracker.objects.filter(
                user=dup['user'],
                date=dup['date']
            ).exclude(
                id=dup['max_id']
            ).delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up duplicate entries'))