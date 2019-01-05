from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
	template_name = 'collection/index.html'
	#template = loader.get_template('collection/index.html')
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'collection/detail.html'
	#return HttpResponse("You're looking at question %s." % question_id)

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'collection/results.html'

def score(request):
	template_name = 'collection/score.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		return render(request, 'collection/score.html', {'collection': c})
		#return Question.objects.order_by('-pub_date')[:5]


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'collection/detail.html', {
			'question':question,
			'error_message': "You didnt select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('collection:results', args=(question.id,)))

# Create your views here.
