# jobs/management/commands/seed_jobs.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from jobs.models import Job
import json

class Command(BaseCommand):
    help = 'Seed the database with jobs'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        one_minute_from_now = now + timezone.timedelta(minutes=1)

        # Example payload for a task
        payload = {
            'func_name': 'example_task',
            'args': ['arg1_value', 'arg2_value'],
            'kwargs': {}
        }

        # Create multiple jobs scheduled for one minute from now
        for i in range(10):
            job = Job(
                payload=json.dumps(payload),
                available_at=one_minute_from_now,
                delay=300  # 5 minutes delay
            )
            job.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created job {job.id}'))
