# jobs/tasks.py
def example_task(arg1, arg2):
    print(f"Executing example_task with arguments: {arg1}, {arg2}")
    # Add your logic here
    return True

ALLOWED_TASKS = {
    'example_task': example_task,
}
