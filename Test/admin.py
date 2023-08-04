from django.contrib import admin

from django.contrib.sessions.models import Session


from Test.models import *
admin.site.register(Candidate)
admin.site.register(Result)
admin.site.register(Question)
admin.site.register(QuestionImages)
admin.site.register(PiChartData)
admin.site.register(QuestionRating)
admin.site.register(Session)
# admin
# Register your models here.
