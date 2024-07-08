# tasks.py
import requests
from polls.models import Question, Choice

def example_task(arg1, arg2):
    print(f"Executing example_task with arguments: {arg1}, {arg2}")
    # Add your logic here
    return True


def get_data_and_insert():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100')
    pokemon_data = response.json()
    pokemon_list = pokemon_data['results']

    # Create the question
    question = Question.objects.create(question_text=question_text, pub_date=timezone.now())

    # Add choices
    for i in range(min(num_choices, len(pokemon_list))):
        choice_text = pokemon_list[i]['name']
        Choice.objects.create(question=question, choice_text=choice_text)

    print(f"Poll created with question: {question_text} and choices: {[pokemon_list[i]['name'] for i in range(num_choices)]}")
    return True


def generate_poll(question_text, num_choices=4):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100')
    pokemon_data = response.json()
    pokemon_list = pokemon_data['results']

    # Create the question
    question = Question.objects.create(question_text=question_text, pub_date=timezone.now())

    # Add choices
    for i in range(min(num_choices, len(pokemon_list))):
        choice_text = pokemon_list[i]['name']
        Choice.objects.create(question=question, choice_text=choice_text)

    print(f"Poll created with question: {question_text} and choices: {[pokemon_list[i]['name'] for i in range(num_choices)]}")
    return True

ALLOWED_TASKS = {
    'example_task': example_task,

    'get_data_and_insert': get_data_and_insert,
    'generate_poll': generate_poll,
}
