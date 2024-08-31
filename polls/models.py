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
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def has_valid_choices(self):
        '''
        Check if the question has 2 or more choices
        '''
        return self.choice_set.count() > 1
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    '''
    Choices for the polls questions
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
