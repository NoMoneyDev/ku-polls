import logging
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Question, Choice, Vote


logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    '''Shows list of available polls'''
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        questions = Question.objects.all()
        ids = [q.id for q in questions
               if (q.is_published() and q.choices_more_than_one())]
        return Question.objects.filter(id__in=ids).order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    '''Shows the choices and let users vote'''
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            question = self.get_object()
        except Http404:
            messages.error(request,
                           'The poll you are trying to access \
                           does not exists.')
            return redirect('polls:index')

        if not question.can_vote():
            messages.error(request,
                           'The poll you are trying to access \
                           is not in the voting period.')
            return redirect('polls:index')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        '''Excludes any questions that aren't published yet.'''
        questions = Question.objects.all()
        ids = [q.id for q in questions if q.is_published()]
        return Question.objects.filter(id__in=ids)


class ResultsView(generic.DetailView):
    '''Shows the result of the polls'''
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    '''
    Used for voting
    '''
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.error(f"{user.username} did not select a choice.")
        messages.error(request, "You didn't select a choice.")
        return redirect('polls:detail', question_id)
    try:
        vote = Vote.objects.filter(choice__question=question, user=user).get()
        logger.info(f"{request.user.username} voted for {selected_choice.choice_text}")
    except (KeyError, Vote.DoesNotExist):
        vote = Vote.objects.create(choice=selected_choice, user=user)
        vote.save()
        return redirect('polls:results', question.id)
    else:
        vote.choice = selected_choice
        messages.success(request, 'Your vote has been recorded.')
        vote.save()
        return redirect('polls:results', question.id)


def signup(request):
    '''Register new user to the site'''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
