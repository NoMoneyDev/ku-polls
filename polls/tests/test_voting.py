import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import authenticate
from polls.models import Question, Vote


def create_question(question_text, days=0, end_day=None,
                    default_pub_date=False, no_choice=False):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    options = {'question_text': question_text}
    if not default_pub_date:
        options['pub_date'] = time
    if end_day:
        end_time = timezone.now() + datetime.timedelta(days=end_day)
        options['end_date'] = end_time
    q = Question.objects.create(**options)
    if not no_choice:
        q.choice_set.create(question=q, choice_text='choice1')
        q.choice_set.create(question=q, choice_text='choice2')
    return q


class QuestionVoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Test', password='test')
        authenticate(username=self.user.username, password='test')
        return super().setUp()

    def vote(self, choice):
        vote = Vote.objects.create(choice=choice, user=self.user)
        vote.save()

    def test_vote_before_pub_date(self):
        '''Test voting on the question before its pub_date'''
        future_question = create_question("future question",
                                          days=5, end_day=10)
        choice = future_question.choice_set.all()[0]
        self.vote(choice)
        self.assertEqual(0, choice.votes)

    def test_vote_after_pub_date(self):
        '''
        Test voting on the question after its pub_date
        but before its end_date
        '''
        present_question = create_question("present question",
                                           days=-5, end_day=5)
        choice = present_question.choice_set.all()[0]
        self.vote(choice)
        self.assertEqual(1, choice.votes)

    def test_vote_after_end_date(self):
        '''Test voting on the question after its end_date'''
        ended_question = create_question("Ended question",
                                         days=-5, end_day=-1)
        choice = ended_question.choice_set.all()[0]
        self.vote(choice)
        self.assertEqual(0, choice.votes)