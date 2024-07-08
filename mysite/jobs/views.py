# jobs/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        job = self.get_object()
        job.reserved_at = timezone.now()
        job.save()

        try:
            payload = job.get_payload()
            func_name = payload['func_name']
            args = payload['args']
            kwargs = payload['kwargs']

            from .tasks import ALLOWED_TASKS
            if func_name in ALLOWED_TASKS:
                task_completed = ALLOWED_TASKS[func_name](*args, **kwargs)
            else:
                raise ValueError(f"Function {func_name} is not allowed")

            if task_completed:
                job.delete()
                return Response({"status": "Job processed successfully"})
            else:
                raise Exception("Task did not complete successfully")
        except Exception as e:
            job.attempts += 1
            job.reserved_at = None
            job.save()
            return Response({"status": f"Failed to process job: {str(e)}"}, status=400)
