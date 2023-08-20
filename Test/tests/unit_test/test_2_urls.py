from django.test import TestCase, Client
from faker import Faker
from Test.models import *
from django.urls import reverse,resolve
from Test.views import *
fake = Faker()

class TestUrls(TestCase):
    def test_home_url(self):
        url = reverse('Test:home')
        self.assertEquals(resolve(url).func , home)
    
    def test_welcome_url(self):
        url = reverse('Test:welcome')
        self.assertEquals(resolve(url).func,welcome)
    
    def test_edit_profile_info_url(self):
        url = reverse('Test:edit_profile_info')
        self.assertEquals(resolve(url).func,edit_profile_info)
    
    def test_testResultHistory_url(self):
        url = reverse('Test:testhistory')
        self.assertEquals(resolve(url).func,testResultHistory)

    def test_candidateRegistration_url(self):
        url = reverse('Test:registrationform')
        self.assertEquals(resolve(url).func,candidateRegistration)
 
    def test_loginView_url(self):
        url = reverse('Test:login')
        self.assertEquals(resolve(url).func,loginView)

    def test_customsTestPaper_url(self):
        url = reverse('Test:customs_test_paper')
        self.assertEquals(resolve(url).func,customsTestPaper)

    def test_calculateTestResult_url(self):
        url = reverse('Test:calculateTest')
        self.assertEquals(resolve(url).func,calculateTestResult)
    
    def test_createTestPaper_url(self):
        url = reverse('Test:setTestPaper')
        self.assertEquals(resolve(url).func,createTestPaper)

    def test_setQuestionSet_url(self):
        url = reverse('Test:setQuestionSet')
        self.assertEquals(resolve(url).func,setQuestionSet)

    def test_startTestPaper_url(self):
        url = reverse('Test:startTestPaper')
        self.assertEquals(resolve(url).func,startTestPaper)

    def test_showTestResult_url(self):
        url = reverse('Test:result')
        self.assertEquals(resolve(url).func,showTestResult)

    def test_logoutView_url(self):
        url = reverse('Test:logout')
        self.assertEquals(resolve(url).func,logoutView)

    def test_uploadQuestion_url(self):
        url = reverse('Test:uploadQuestion')
        self.assertEquals(resolve(url).func,uploadQuestion)

    def test_NIMCET_Test_url(self):
        url = reverse('Test:NIMCET_Test')
        self.assertEquals(resolve(url).func,NIMCET_Test)

    def test_compete_url(self):
        url = reverse('Test:compete')
        self.assertEquals(resolve(url).func,compete)

    def test_account_url(self):
        url = reverse('Test:account')
        self.assertEquals(resolve(url).func,account)

class TestViews(TestCase):
    def setUp(self):
        self.username = fake.user_name()
        self.password = fake.password()
        self.name = fake.name()
        self.candidate = Candidate.objects.create(
                username =  self.username ,
                password = self.password,
                name = self.name

            )
        self.client = Client()
    
    def test_home_page(self):
        response = self.client.get(reverse('Test:home'))
        self.assertEqual(response.status_code, 302)


    # Test for checking signUp page working properly
    def test_sign_up_page(self):
        data =  {'username':self.username ,
                  'password':self.password ,
                  'name':self.name}
        response = self.client.post(reverse('Test:registrationform'),data=data)
        self.assertEqual(response.status_code,302) 


    # 200 for OK
    def test_login_page(self):
        response = self.client.get(reverse('Test:login'))
        self.assertEqual(response.status_code, 200)

    # check for successful login
    def test_login_success(self):
        response = self.client.post(reverse('Test:login'),{'username':self.username,'password':self.password})
        print('Login successful')
        self.assertEqual(response.status_code,302) 

    # check for  login  fail
    def test_login_success(self):
        response = self.client.post(reverse('Test:login'),{'username':self.username,'password':self.password})
        self.assertEqual(response.status_code,200) 

    #check whether test paper starts
    def test_start_paper(self):
        response = self.client.post(reverse('Test:testpaper'),{'n':1 })
        self.assertEqual(response.status_code, 200)



    