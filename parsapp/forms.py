from django import forms
from parsapp.models import WordContext


class ParseForm(forms.Form):
	parse_text = forms.CharField(widget=forms.Textarea, label="Introduce the text to learn from")

class WordContextForm(forms.ModelForm):
	status = forms.ChoiceField(choices = [(1,"Ignore"),(2,"Learned"),(3,"To learn")])
	class Meta:
		model = WordContext
		fields = ('status',)
	def __init__(self, *args, **kwargs):
		super(WordContextForm, self).__init__(*args, **kwargs)
		self.fields['status'].label = self.instance.word.name
		# TODO: if status==0, choices Ignore,To Learn. If status==2,3, choices Learned, To Learn

	
