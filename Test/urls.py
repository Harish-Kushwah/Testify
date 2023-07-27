from django.urls import path
from Test.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Test'

urlpatterns = [
    path('', welcome,name = 'welcome'),
    path('test-history',testResultHistory ,name = 'testhistory'),
    path('registrationform', candidateRegistration , name ='registrationform' ),
    path('login', loginView, name = 'login'),
    path('home', candidateHome , name='home'),
    path('test-paper',testPaper,name = 'testpaper'),
    path('customs-test-paper',customsTestPaper,name = 'customs_test_paper'),
    path('calculate-result',calculateTestResult ,name="calculateTest"),
    path('result',showTestResult , name = 'result'),
    path('logout',logoutView , name = 'logout'),
    path('uploadQuestion',uploadQuestion , name = 'uploadQuestion'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )