from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        questions = Question.objects.all()
        ids = [q.id for q in questions if (q.is_published() and q.choices_more_than_one())]
        return Question.objects.filter(id__in=ids).order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            question = self.get_object()
        except Http404:
            messages.error(request, 'The poll you are trying to access does not exists.')
            return redirect('polls:index')
        
        if not question.can_vote():
            messages.error(request, 'The poll you are trying to access is not in the voting period.')
            return redirect('polls:index')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        '''Excludes any questions that aren't published yet.'''
        questions = Question.objects.all()
        ids = [q.id for q in questions if q.is_published()]
        return Question.objects.filter(id__in=ids)
    


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.vote()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
