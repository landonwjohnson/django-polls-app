from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from django.utils import timezone
from datetime import datetime, timedelta
from jobs.models import Job
from jobs.tasks import ALLOWED_TASKS
import json
import time
import logging
import pytz

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
        payload = json.loads(job.payload)
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

def create_quarterly_job(scheduler, func_name, args=[], kwargs={}):
    current_time = datetime.now(pytz.UTC)
    for i in range(1, 5):  # Four quarters in a year
        next_date = current_time + timedelta(days=(i * 90) + 30)  # 90 days per quarter + 30 days

        # Check for duplicate jobs
        existing_jobs = Job.objects.filter(
            available_at=next_date,
            reserved_at__isnull=True
        )

        if existing_jobs.exists():
            logger.info(f"Job for {next_date} already exists. Skipping creation.")
            continue

        payload = json.dumps({
            'func_name': func_name,
            'args': args,
            'kwargs': kwargs
        })

        job = Job.objects.create(
            payload=payload,
            available_at=next_date
        )

        scheduler.add_job(
            process_job,
            trigger=DateTrigger(run_date=next_date),
            id=f"quarterly_job_{i}",
            replace_existing=True,
            args=[job]
        )

        logger.info(f"Created job for {next_date}")

def start():
    scheduler = BackgroundScheduler()

    # Schedule the job function to be called every other hour
    scheduler.add_job(process_jobs, CronTrigger(minute=0, hour='*/2'), id="process_jobs", replace_existing=True)

    # Schedule the daily check job
    scheduler.add_job(process_jobs, CronTrigger(hour='0', minute='0'), id="daily_check_job", replace_existing=True)

    # Schedule the quarterly job with an additional 30 days
    create_quarterly_job(scheduler, 'get_data_and_insert')  # Replace 'my_task_function' with your actual task function name

    scheduler.start()
    logger.info("Scheduler started...")

# Ensure you start the scheduler when the Django app starts
if __name__ == "__main__":
    start()
