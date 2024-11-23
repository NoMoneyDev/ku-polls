import datetime
from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    '''
    Questions model include question_text and published date
    along with methods to check if the question was pulished recently (<= 1day)
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=now)
    end_date = models.DateTimeField("date expired", null=True)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        '''
        Check if the question was pulished recently (<= 1day)
        '''
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    def choices_more_than_one(self):
        '''
        Check if the question has 2 or more choices
        '''
        return self.choice_set.count() > 1

    def is_published(self):
        '''Check if the question is past its publication time'''
        return timezone.now() >= self.pub_date

    def can_vote(self):
        '''Check if the question is after pub_date and before end_date'''
        now = timezone.now()
        return self.is_published() and \
            (self.end_date is None or now <= self.end_date)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    '''
    Choices for the polls questions
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        '''Return the number of votes for this choice'''
        return Vote.objects.filter(choice=self).count()

    @property
    def percent(self):
        '''
        Turn votes in this choice to percentage
        '''
        all_votes = sum(choice.votes for choice in
                        self.question.choice_set.all())
        if all_votes == 0:
            return '0.00%'
        return f"{self.votes/all_votes*100:.2f}%"

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        question = self.choice.question
        if question.can_vote():
            return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} : {self.choice.choice_text}"
