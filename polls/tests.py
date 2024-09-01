from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
import datetime

# Create your tests here.


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


class QuestionIndexViewTests(TestCase):
    '''
    Test if questions show up when there are no_choice, past its pub_date,
    its pub_date is in the future, or no questions at all.
    '''
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context_data['questions_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context_data['questions_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context_data['questions_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context_data['questions_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context_data['questions_list'],
            [question2, question1], ordered=False,
        )

    def test_question_with_no_choice(self):
        """
        The questions index page doesn't display questions without choices.
        """
        create_question(question_text='No Choice.',
                        days=-30, no_choice=True)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context_data['questions_list'],
            [],
        )


class QuestionDetailViewTests(TestCase):
    '''
    Test detail view if it shows past questions, or future questions.
    '''
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionIsPublishedTest(TestCase):
    '''
    Test is_published() method with past, default, and future questions.
    '''
    def test_past_question(self):
        '''
        Test is_published() in Question and check if it shows up in index view
        '''
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:index')
        self.assertTrue(past_question.is_published())
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_default_question(self):
        default_question = create_question(question_text='Default Question.',
                                           default_pub_date=True)
        url = reverse('polls:index')
        self.assertTrue(default_question.is_published())
        response = self.client.get(url)
        self.assertContains(response, default_question.question_text)

    def test_future_question(self):
        future_question = create_question(question_text='Future Question.',
                                          days=5)
        url = reverse('polls:index')
        self.assertFalse(future_question.is_published())
        response = self.client.get(url)
        self.assertNotContains(response, future_question.question_text)


class QuestionCanVoteTest(TestCase):
    '''
    Test can_vote() in Question and test if you can vote
    '''
    def test_cannot_vote_before_pub_date(self):
        '''Test can_vote() with question that hasn't been published'''
        future_question = create_question("future question",
                                          days=5, end_day=10)
        choice = future_question.choice_set.all()[0]
        self.assertFalse(future_question.can_vote())
        self.assertFalse(choice.vote())
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
        self.assertTrue(choice.vote())
        self.assertEqual(1, choice.votes)

    def test_cannot_vote_after_end_date(self):
        '''
        Test can_vote() with question that has passed its end_date
        '''
        ended_question = create_question("Ended question",
                                         days=-5, end_day=-1)
        choice = ended_question.choice_set.all()[0]
        self.assertFalse(ended_question.can_vote())
        self.assertFalse(choice.vote())
        self.assertEqual(0, choice.votes)

    def test_can_vote_last_second(self):
        '''
        Test can_vote() at the exact time poll is ending
        '''
        last_sec_question = create_question(question_text='last_sec',
                                            end_day=0)
        choice = last_sec_question.choice_set.all()[0]
        self.assertTrue(last_sec_question.can_vote())
        self.assertTrue(choice.vote())
        self.assertEqual(1, choice.votes)


class QuestionVoteTest(TestCase):
    def test_vote_before_pub_date(self):
        '''Test voting on the question before its pub_date'''
        future_question = create_question("future question",
                                          days=5, end_day=10)
        choice = future_question.choice_set.all()[0]
        self.assertFalse(choice.vote())
        self.assertEqual(0, choice.votes)

    def test_vote_after_pub_date(self):
        '''
        Test voting on the question after its pub_date
        but before its end_date
        '''
        present_question = create_question("present question",
                                           days=-5, end_day=5)
        choice = present_question.choice_set.all()[0]
        self.assertTrue(choice.vote())
        self.assertEqual(1, choice.votes)

    def test_vote_after_end_date(self):
        '''Test voting on the question after its end_date'''
        ended_question = create_question("Ended question",
                                         days=-5, end_day=-1)
        choice = ended_question.choice_set.all()[0]
        self.assertFalse(choice.vote())
        self.assertEqual(0, choice.votes)
