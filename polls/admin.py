from django.contrib import admin
from .models import Question, Choice

# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    fieldssets = [
        (None, {'fields': ['question_text']}),
        ("Date Information", {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInLine]
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
