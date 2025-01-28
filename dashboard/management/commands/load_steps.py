from django.core.management.base import BaseCommand
from dashboard.models import StepTracker, UserProfile
from datetime import datetime
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Load mock step data from mock_data/steps.json"

    def handle(self, *args, **kwargs):
        # Get the project root directory
        project_root = settings.BASE_DIR
        file_path = os.path.join(project_root, "mock_data", "steps.json")
        
        self.stdout.write(f"Attempting to load file from: {file_path}")

        try:
            with open(file_path, "r") as file:
                mock_data = json.load(file)
                
            # Get your admin user's profile
            try:
                user_profile = UserProfile.objects.get(user__username='mayazhang')
                self.stdout.write(f"Found user profile for: {user_profile}")
            except UserProfile.DoesNotExist:
                self.stdout.write(self.style.ERROR("Admin user profile not found"))
                return

            count = 0
            for record in mock_data:
                try:
                    date = datetime.strptime(record['date'], '%m/%d/%Y').date()
                    steps = int(record['steps'])
                    
                    # Use get_or_create to avoid duplicates
                    step_entry, created = StepTracker.objects.get_or_create(
                        user=user_profile,
                        date=date,
                        defaults={'steps': steps}
                    )
                    
                    if created:
                        count += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing record: {record}. Error: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {count} step records"))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found at {file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format in steps.json"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))


