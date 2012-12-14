from django import forms
from parsapp.models import WordContext

class ParseForm(forms.Form):
	parse_text = forms.CharField(widget=forms.Textarea, label="Introduce the text to learn from")

class WordContextForm(forms.ModelForm):
	status = forms.ChoiceField(choices = [(1,"Ignore"),(3,"Tolearn")] )
	class Meta:
		model = WordContext
		fields = ('word', 'status')



