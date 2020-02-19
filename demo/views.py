from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice

# Create your views here.
def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_questions}
    return render(request, 'demo/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)    
    return render(request, 'demo/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'demo/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,
            'demo/detail.html', {'question': question, 'error_message': "You did not select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('demo:results', args=(question.id,)))
