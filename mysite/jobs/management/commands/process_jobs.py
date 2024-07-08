# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from jobs.models import Job
from jobs.tasks import ALLOWED_TASKS
import time
import logging

logger = logging.getLogger(__name__)

def process_jobs():
    now = timezone.now()
    batch_size = 10  # Define the size of the batch to process at a time
    jobs = Job.objects.filter(available_at__lte=now, reserved_at__isnull=True).order_by('available_at')[:batch_size]

    if not jobs.exists():
        logger.info("All jobs have been completed.")
        return

    for job in jobs:
        time.sleep(job.delay)  # Consider replacing this with a non-blocking delay if possible
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
        logger.error(f'Failed to process job {job.id}: {str(e)}')

def start():
    scheduler = BackgroundScheduler()

    # Schedule the job function to be called every other hour
    scheduler.add_job(process_jobs, CronTrigger(minute=0, hour='*/2'), id="process_jobs", replace_existing=True)

    scheduler.start()
    logger.info("Scheduler started...")

# Ensure you start the scheduler when the Django app starts
if __name__ == "__main__":
    start()
