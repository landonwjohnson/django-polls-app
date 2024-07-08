# jobs/models.py
from django.db import models
from django.utils import timezone
import json

class Job(models.Model):
    payload = models.TextField()  # Store function name and arguments as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    queue = models.CharField(max_length=255, default='default')
    reserved_at = models.DateTimeField(null=True, blank=True)
    available_at = models.DateTimeField(default=timezone.now)
    attempts = models.PositiveIntegerField(default=0)
    delay = models.PositiveIntegerField(default=300)  # Delay in seconds (default 5 minutes)

    def __str__(self):
        return f"Job {self.id} in queue {self.queue}"

    class Meta:
        db_table = 'jobs'

    def set_payload(self, func_name, *args, **kwargs):
        self.payload = json.dumps({
            'func_name': func_name,
            'args': args,
            'kwargs': kwargs
        })

    def get_payload(self):
        return json.loads(self.payload)
