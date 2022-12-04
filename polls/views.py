from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader 
from django.http import Http404
from django.urls import reverse
from django.views import generic 
from django.utils import timezone

class IndexView(generic.ListView):
    # latest_questions_list = Question.objects.order_by('-pub_date')[:5]
    # # output = ' ,'.join([q.question_text for q in latest_questions_list])
    # # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_questions_list': latest_questions_list
    # }
    # # return HttpResponse(template.render(context, request))
    # return render(request, 'polls/index.html', context)
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailsView(generic.DetailView):
    model = Question 
    template_name = 'polls/details.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question 
    template_name = 'polls/results.html'
# def details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("The Question does not exist")
#     return render(request, 'polls/details.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question, "success": "Thank you for voting"})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html',{
            'question': question,
            'error_message': 'Please select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
# Create your views here.
