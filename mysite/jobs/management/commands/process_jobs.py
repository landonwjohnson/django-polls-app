# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from jobs.models import Job  # Adjust the import based on your app structure

def process_jobs():
    now = timezone.now()
    jobs = Job.objects.filter(available_at__lte=now, reserved_at__isnull=True)
    
    for job in jobs:
        process_job(job)

def process_job(job):
    # Mark job as reserved
    job.reserved_aa# scheduler.py
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
        process_job(job)
        time.sleep(300)  # Wait for 5 minutes before processing the next job

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
 = timezone.now()
    job.save()

    try:
        # Process the job
        # Deserialize the payload and perform the task
        payload = job.payload
        # (Add your job processing logic here)
        print(f'Processing job {job.id} with payload: {payload}')
        
        # Mark job as completed (delete or archive)
        job.delete()
    except Exception as e:
        # Handle exceptions (logging, retry logic, etc.)
        job.attempts += 1
        job.reserved_at = None
        job.save()
        print(f'Failed to process job {job.id}: {str(e)}')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Schedule the job function to be called every night at midnight
    scheduler.add_job(process_jobs, CronTrigger(hour=0, minute=0), id="process_jobs", replace_existing=True)
    
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
