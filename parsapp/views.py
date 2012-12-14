from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from parsapp.models import Word, WordContext
from parsapp.forms import ParseForm, WordContextForm


import re
import dump # load english_dict with top 1000 UK words


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

@login_required
def parse_input(request):
	if request.method=='POST':
		form = ParseForm(request.POST)
		if form.is_valid():
			msg = form.cleaned_data['parse_text']
			msg = dump.select_words(msg, request)
			for word in msg: #Include them in temp phase
				try:
					w = Word.objects.get(name=word)
				except Word.DoesNotExist:
					# TODO: What if word does not exists in dictionary?
					w = Word.objects.create(name=word, description="TODO")
				request.user.wordcontext_set.create( word=w, status=0) #status temp
			return	HttpResponseRedirect(reverse('words', kwargs={'status':0}))
	else:
		form = ParseForm(initial={'parse_text':'What text do you want to fucking parse?'})
	return render_to_response('parse_form.html', 
		{'form':form},
		context_instance = RequestContext(request),
		)

@login_required
def word_view(request, status):
	WordFormSet = inlineformset_factory(User, WordContext, 
		fk_name="user", can_delete=False, extra=0, form=WordContextForm)
	
	class WordFormSetFiltered(WordFormSet):
		def get_queryset(self):
			## See get_queryset method of django.forms.models.BaseModelFormSet
			if not hasattr(self, '_queryset'):
				self._queryset = self.queryset.filter(status=status)
				if not self._queryset.ordered:
					self._queryset = self._queryset.order_by(self.model._meta.pk.name) 
				# assert False               
			return self._queryset



	if request.method=='POST':
		formset = WordFormSetFiltered(request.POST, instance=request.user)
		if formset.is_valid():
			formset.save()
			return render_to_response('congrats.html')
	else:
		formset = WordFormSetFiltered(instance=request.user)
	return render_to_response('words_form.html',
		{'formset':formset},
		context_instance = RequestContext(request),
		)

	



