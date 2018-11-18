from django.contrib import admin
from poll.models import Question, Choice, Answer

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
