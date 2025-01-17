import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_returns_false_for_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_returns_false_for_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_returns_true_for_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class IndexViewTests(TestCase):
    
    def test_no_questions(self):
        response = self.client.get(reverse('demo:index'))        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('demo:index'))        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_future_question(self):
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('demo:index'))        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question_and_future_question(self):
        create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('demo:index'))        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_two_past_questions(self):
        create_question(question_text="Past question 1", days=-30)
        create_question(question_text="Past question 2", days=-3)
        response = self.client.get(reverse('demo:index'))        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2>', '<Question: Past question 1>'])

class DetailViewTest(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text="Future question", days=3)
        url = reverse('demo:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse('demo:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
