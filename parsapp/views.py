from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from parsapp.models import Word, WordContext
from parsapp.forms import ParseForm, WordContextForm
from parsapp.dictionary import lookup

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
					w = Word.objects.create(name=word, description=lookup(word))
				request.user.wordcontext_set.create( word=w, status=0) #status temp
			return	HttpResponseRedirect(reverse('words', kwargs={'status':0}))
	else:
		form = ParseForm(initial={'parse_text':'The hacker made the startup! Parse it!'})
	return render_to_response('parse_form.html', 
		{'form':form},
		context_instance = RequestContext(request),
		)

@login_required
def word_view(request, status):
	WordFormSet = inlineformset_factory(User, WordContext, 
		fk_name="user", can_delete=False, extra=0, form=WordContextForm)
	if request.method=='POST':
		formset = WordFormSet(request.POST, instance=request.user)
		if formset.is_valid():
			formset.save()
			return render_to_response('congrats.html', context_instance = RequestContext(request))
	else:
		formset = WordFormSet(instance=request.user, queryset=WordContext.objects.filter(status=status))
	return render_to_response('words_form.html',
		{'formset':formset},
		context_instance = RequestContext(request),
		)

	



