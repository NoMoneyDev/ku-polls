from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Question

# Create your views here.

def index(request):
    questions_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'questions_list' : questions_list
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = f'You are looking at results of question : {question_id}'
    return HttpResponse(response)

def vote(request, question_id):
    response = f'You are voting on question {question_id}'
    return HttpResponse(response)
