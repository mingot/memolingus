from django.contrib import admin
from parsapp.models import Word

class WordAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'words_tolearn', 'words_known')
	search_fields = ('user_id')

admin.site.register(Word)

