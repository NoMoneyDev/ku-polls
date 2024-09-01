from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.utils.timezone import now
import datetime


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
        return self.is_published() and (self.end_date is None or now <= self.end_date)
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    '''
    Choices for the polls questions
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def vote(self):
        '''
        Cast a vote if able to, then return True if voted succesfully else False
        '''
        if self.question.can_vote():
            self.votes += 1
            self.save()
            return True
        return False

    @property
    def percent(self):
        '''
        Turn votes in this choice to percentage
        '''
        all_votes = sum(choice.votes for choice in self.question.choice_set.all())
        if all_votes == 0:
            return '0.00%'
        return f"{self.votes/all_votes*100:.2f}%"


    def __str__(self):
        return self.choice_text
