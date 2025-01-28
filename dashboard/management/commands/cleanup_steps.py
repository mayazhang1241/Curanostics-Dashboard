from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Clean up duplicate step tracker entries'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Delete duplicates keeping the latest entry for each user-date combination
            cursor.execute("""
                DELETE FROM dashboard_steptracker
                WHERE id NOT IN (
                    SELECT MAX(id)
                    FROM dashboard_steptracker
                    GROUP BY user_id, date
                );
            """)
            
            self.stdout.write(self.style.SUCCESS('Successfully cleaned up duplicate entries'))
            