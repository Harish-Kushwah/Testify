from django.contrib import admin

from django.contrib.sessions.models import Session


from Test.models import *
admin.site.register(Candidate)
admin.site.register(Result)
admin.site.register(QuestionImages)
admin.site.register(QuestionRating)
admin.site.register(Session)
admin.site.register(TestPaperSet)
admin.site.register(QuestionSet)
admin.site.register(DiscussRoom)

