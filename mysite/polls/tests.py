from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import Question, Choice
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .serializers import QuestionSerializer, ChoiceSerializer


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class QuestionModelTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.question_data = {
            'question_text': 'What is your favorite color?',
            'pub_date': timezone.now()
        }
        self.question = Question.objects.create(**self.question_data)
        self.choice_data = {
            'question': self.question,
            'choice_text': 'Blue',
            'votes': 0
        }
        self.choice = Choice.objects.create(**self.choice_data)

    def test_create_question(self):
        url = reverse('polls:question-list')
        response = self.client.post(url, self.question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)  # One created in setUp and one in test

    def test_read_question(self):
        url = reverse('polls:question-detail', args=[self.question.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, QuestionSerializer(self.question).data)

    def test_update_question(self):
        url = reverse('polls:question-detail', args=[self.question.id])
        updated_data = {
            'question_text': 'What is your favorite animal?',
            'pub_date': timezone.now()
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, updated_data['question_text'])

    def test_delete_question(self):
        url = reverse('polls:question-detail', args=[self.question.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)


class ChoiceAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.question = Question.objects.create(
            question_text='What is your favorite color?',
            pub_date=timezone.now()
        )
        self.choice_data = {
            'question': self.question.id,
            'choice_text': 'Blue',
            'votes': 0
        }
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='Blue',
            votes=0
        )

    def test_create_choice(self):
        url = reverse('polls:choice-list')
        response = self.client.post(url, self.choice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Choice.objects.count(), 2)  # One created in setUp and one in test

    def test_read_choice(self):
        url = reverse('polls:choice-detail', args=[self.choice.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ChoiceSerializer(self.choice).data)

    def test_update_choice(self):
        url = reverse('polls:choice-detail', args=[self.choice.id])
        updated_data = {
            'question': self.question.id,
            'choice_text': 'Green',
            'votes': 1
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.choice_text, updated_data['choice_text'])
        self.assertEqual(self.choice.votes, updated_data['votes'])

    def test_delete_choice(self):
        url = reverse('polls:choice-detail', args=[self.choice.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Choice.objects.count(), 0)
