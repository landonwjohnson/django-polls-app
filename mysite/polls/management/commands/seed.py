import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.models import Question, Choice

class Command(BaseCommand):
    help = 'Seed the database with some sample data'

    python_facts = {
        "What is Python?": "Python is a high-level, interpreted programming language known for its easy-to-read syntax and dynamic typing.",
        "Who created Python and when?": "Python was created by Guido van Rossum and was first released in 1991.",
        "What are Python's key features?": "Python is known for its simplicity, readability, and versatility. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.",
        "What is PEP 8?": "PEP 8 is the Python Enhancement Proposal which outlines the conventions for writing clean, readable Python code.",
        "What is the Python Package Index (PyPI)?": "PyPI is a repository of software for the Python programming language. It helps you find and install software developed and shared by the Python community.",
        "What are Python's built-in data types?": "Python's built-in data types include integers, floats, strings, lists, tuples, sets, and dictionaries.",
        "What is a list comprehension?": "A list comprehension is a concise way to create lists in Python. It consists of brackets containing an expression followed by a for clause, and optionally one or more if clauses.",
        "What is a lambda function?": "A lambda function is an anonymous, inline function defined with the lambda keyword. It can take any number of arguments but only one expression.",
        "What is the difference between a list and a tuple?": "The main difference is that lists are mutable, meaning their elements can be changed, while tuples are immutable, meaning their elements cannot be changed once assigned.",
        "How does Python handle memory management?": "Python uses automatic memory management, including garbage collection, to handle memory allocation and deallocation.",
        "What is a Python decorator?": "A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure.",
        "What are Python's built-in modules?": "Python has a rich standard library that includes modules like os, sys, math, datetime, json, re, and many others.",
        "What is the Global Interpreter Lock (GIL)?": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This means only one thread can execute Python code at a time, even on multi-core systems.",
        "What is a virtual environment?": "A virtual environment in Python is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages.",
        "What is a module and a package in Python?": "A module is a single file (or files) that are imported under one import and used. A package is a collection of modules in directories that give a package hierarchy.",
        "What is the use of 'self' in Python?": "The 'self' keyword is used in instance methods to refer to the instance on which the method is being called. It is the first parameter of methods in a class.",
        "What is the difference between Python 2 and Python 3?": "Python 3 is the newer version, released in 2008, which is not backward-compatible with Python 2. It includes many improvements and optimizations, such as better Unicode support and a more consistent syntax.",
        "What are Python's built-in functions?": "Python has many built-in functions like print(), len(), range(), type(), int(), float(), str(), and many more.",
        "How do you handle exceptions in Python?": "Exceptions in Python are handled using try-except blocks. You can also use finally to execute code after the try-except block regardless of whether an exception occurred.",
        "What is a docstring?": "A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition. It is used to document the object.",
        "What is list slicing?": "List slicing is a way to get a subset of a list using a special syntax: list[start:end:step]. It can be used to access parts of the list.",
        "What is the difference between '==' and 'is' in Python?": "'==' checks for value equality, whereas 'is' checks for identity (i.e., whether the objects are the same instance).",
        "What are Python's loop control statements?": "Python's loop control statements include break (exits the loop), continue (skips to the next iteration), and pass (a null statement used as a placeholder).",
        "What is the use of the 'with' statement in Python?": "The 'with' statement is used for resource management and exception handling. It ensures that resources are properly cleaned up after use, such as file streams.",
    }

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        self._create_or_update_questions_with_choices()
        self.stdout.write('Database successfully seeded.')

    def _create_or_update_questions_with_choices(self):
        for question_text, answer_text in self.python_facts.items():
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'pub_date': timezone.now()}
            )
            if created or not question.choice_set.exists():
                self._add_choices_to_question(question, answer_text)
            else:
                self._ensure_minimum_choices(question, answer_text)

    def _add_choices_to_question(self, question, answer_text):
        choices_text = [
            answer_text,
            f'Alternate answer: {answer_text[:50]}...'
        ]
        for choice_text in choices_text:
            Choice.objects.get_or_create(
                question=question,
                choice_text=choice_text,
                defaults={'votes': random.randint(0, 100)}
            )

    def _ensure_minimum_choices(self, question, answer_text):
        if question.choice_set.count() < 2:
            existing_choices = question.choice_set.values_list('choice_text', flat=True)
            if answer_text not in existing_choices:
                Choice.objects.create(
                    question=question,
                    choice_text=answer_text,
                    votes=random.randint(0, 100)
                )
            if f'Alternate answer: {answer_text[:50]}...' not in existing_choices:
                Choice.objects.create(
                    question=question,
                    choice_text=f'Alternate answer: {answer_text[:50]}...',
                    votes=random.randint(0, 100)
                )

