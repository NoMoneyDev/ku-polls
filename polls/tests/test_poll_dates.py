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


class QuestionModelTests(TestCase):
    '''
    Test wes_published_recently()
    in Question with old, recent, and future questions.
    '''
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

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
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionCanVoteTest(TestCase):
    '''
    Test can_vote() in Question and test if you can vote
    '''
    def setUp(self):
        self.user = User.objects.create_user('Test', password='test')
        authenticate(username=self.user.username, password='test')
        return super().setUp()

    def vote(self, choice):
        vote = Vote.objects.create(choice=choice, user=self.user)
        vote.save()

    def test_cannot_vote_before_pub_date(self):
        '''Test can_vote() with question that hasn't been published'''
        future_question = create_question("future question",
                                          days=5, end_day=10)
        choice = future_question.choice_set.all()[0]
        self.assertFalse(future_question.can_vote())
        self.vote(choice)
        self.assertEqual(0, choice.votes)

    def test_can_vote_after_pub_date(self):
        '''
        Test can_vote() with question that has passed its published date
        but not end_date
        '''
        present_question = create_question("present question",
                                           days=-5, end_day=5)
        choice = present_question.choice_set.all()[0]
        self.assertTrue(present_question.can_vote())
        self.vote(choice)
        self.assertEqual(1, choice.votes)

    def test_cannot_vote_after_end_date(self):
        '''
        Test can_vote() with question that has passed its end_date
        '''
        ended_question = create_question("Ended question",
                                         days=-5, end_day=-1)
        choice = ended_question.choice_set.all()[0]
        self.assertFalse(ended_question.can_vote())
        self.vote(choice)
        self.assertEqual(0, choice.votes)

    def test_can_vote_last_second(self):
        '''
        Test can_vote() at the exact time poll is ending
        '''
        last_sec_question = create_question(question_text='last_sec',
                                            end_day=0)
        choice = last_sec_question.choice_set.all()[0]
        self.assertTrue(last_sec_question.can_vote())
        self.vote(choice)
        self.assertEqual(1, choice.votes)
