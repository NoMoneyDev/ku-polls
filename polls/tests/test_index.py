from django.test import TestCase
from django.urls import reverse


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