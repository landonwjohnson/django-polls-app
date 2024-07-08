# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from jobs.models import Job
from jobs.tasks import ALLOWED_TASKS
import time

def process_jobs():
    now = timezone.now()
    jobs = Job.objects.filter(available_at__lte=now, reserved_at__isnull=True).order_by('available_at')
    
    for job in jobs:
        time.sleep(job.delay)  # Wait for the specified delay before processing the next job
        process_job(job)

def process_job(job):
    # Mark job as reserved
    job.reserved_at = timezone.now()
    job.save()

    try:
        # Deserialize the payload and perform the task
        payload = job.get_payload()
        func_name = payload['func_name']
        args = payload['args']
        kwargs = payload['kwargs']

        if func_name in ALLOWED_TASKS:
            task_completed = ALLOWED_TASKS[func_name](*args, **kwargs)
        else:
            raise ValueError(f"Function {func_name} is not allowed")

        if task_completed:
            # Mark job as completed (delete or archive)
            job.delete()
        else:
            raise Exception("Task did not complete successfully")
    except Exception as e:
        # Handle exceptions (logging, retry logic, etc.)
        job.attempts += 1
        job.reserved_at = None
        job.save()
        print(f'Failed to process job {job.id}: {str(e)}')

def start():
    scheduler = BackgroundScheduler()

    # Schedule the job function to be called every minute
    scheduler.add_job(process_jobs, CronTrigger(minute='*'), id="process_jobs", replace_existing=True)

    scheduler.start()
    print("Scheduler started...")
