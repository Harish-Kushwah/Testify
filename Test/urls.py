from django.urls import path
from Test.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Test'

urlpatterns = [
    path('', welcome,name = 'welcome'),
    path('account', account,name = 'account'),
    path('edit_profile_info', edit_profile_info,name = 'edit_profile_info'),
    path('test-history',testResultHistory ,name = 'testhistory'),
    path('registrationform', candidateRegistration , name ='registrationform' ),
    path('login', loginView, name = 'login'),
    path('home', candidateHome , name='home'),
    path('test-paper',testPaper,name = 'testpaper'),
    path('customs-test-paper',customsTestPaper,name = 'customs_test_paper'),
    path('calculate-result',calculateTestResult ,name="calculateTest"),
    path('set-test-paper',createTestPaper ,name="setTestPaper"),
    path('set-question-set',setQuestionSet ,name="setQuestionSet"),
    path('start-test-paper',startTestPaper ,name="startTestPaper"),
    path('result',showTestResult , name = 'result'),
    path('logout',logoutView , name = 'logout'),
    path('uploadQuestion',uploadQuestion , name = 'uploadQuestion'),
    path('NIMCET_Test',NIMCET_Test , name = 'NIMCET_Test'),
    path('compete',compete , name = 'compete'),

  



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )