from django import forms
from parsapp.models import WordContext


class ParseForm(forms.Form):
	parse_text = forms.CharField(widget=forms.Textarea(attrs={'style':'margin: 0px; width: 742px; height: 301px;'}), label="Introduce the text to learn from")

class WordContextForm(forms.ModelForm):
	status = forms.ChoiceField(choices = [(2,"Learned"),(3,"To learn")])
	class Meta:
		model = WordContext
		fields = ('status',)
	def __init__(self, *args, **kwargs):
		super(WordContextForm, self).__init__(*args, **kwargs)
		self.fields['status'].label = self.instance.word.name
		if self.instance.status == 0:
			self.fields['status'].choices=[(1,"Ignore"),(3,"To learn")]

