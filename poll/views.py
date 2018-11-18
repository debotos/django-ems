from django.shortcuts import render, get_object_or_404, reverse, redirect
from poll.models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.http import HttpResponse, Http404, HttpResponseRedirect

from ems.decorators import admin_hr_required, admin_only
from poll.forms import PollForm, ChoiceForm
from poll.models import *

# pylint: disable=E1101


class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/list/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question)
        question.delete()
        return redirect('polls_list')


@login_required(login_url="/login/")
def index(request):
    context = {}
    questions = Question.objects.all()
    context['questions'] = questions
    context['title'] = 'polls'
    return render(request, 'polls/index.html', context)


@login_required(login_url="/login/")
def details(request, id=None):
    context = {}
    question = get_object_or_404(Question, pk=id)
    context['question'] = question
    return render(request, 'polls/details.html', context)


@login_required(login_url="/login/")
def vote_poll(request, id=None):
    print(request)
    if request.method == "GET":
        context = {}
        question = get_object_or_404(Question, pk=id)
        context['question'] = question
        return render(request, 'polls/poll.html', context)

    if request.method == "POST":
        data = request.POST
        user_id = 1
        # although Answer Model want user and choice obj but
        # to make it work just using id provide **kwargs as
        # user_id and choice_id
        res = Answer.objects.create(user_id=user_id, choice_id=data['answer'])

        if res:
            return HttpResponse("Your vote is done successfully")
        else:
            return HttpResponse("Failed to vote")