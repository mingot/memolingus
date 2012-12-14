from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
	name = models.CharField(max_length=10)
	description = models.CharField(max_length=10000)

	def __unicode__(self):
		return u'%s' % self.name

class WordContext(models.Model):
	user = models.ForeignKey(User)
	word = models.ForeignKey(Word)
	date = models.DateField(null=True)
	status = models.SmallIntegerField() # 0: Temp, 1: Ignore, 2: Known, 3: To learn 
	context = models.CharField(max_length=100, null=True)

	def __unicode__(self):
		return u'word:%s, user:%s' % (self.word.name, self.user.username)