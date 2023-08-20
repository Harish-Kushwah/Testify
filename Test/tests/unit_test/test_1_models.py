from django.test import TestCase, Client ,RequestFactory,selenium
from faker import Faker
from Test.models import *
from django.urls import reverse,resolve
from Test.views import *


fake = Faker()
import random
from datetime import datetime
# Tt run the tests command is
#> python manage.py test Test.tests.unit_test.TestModels

class TestModels(TestCase):
    def setUp(self):
      self.total_obj_should_create = 10
      self.paper_set_list = []

    # check whether the candidate model is creating successfully
    def test_candidate(self):
        for i in range(0,self.total_obj_should_create):
            username = fake.user_name()
            password = fake.password()
            name = fake.name()
            test_attempted = random.randint(0,10000)
            email = fake.email()
            candidate =  Candidate.objects.create(username=username,
                                            password=password,
                                            name=name,
                                            test_attempted=test_attempted,
                                            email = email,
                                            )
            self.assertEqual(candidate.username,username )
            self.assertEqual(candidate.test_attempted,test_attempted)
            self.assertEqual(candidate.about ,None)
            self.assertEqual(candidate.contact_no ,None)
        print("first")
        total_candidate_created = Candidate.objects.all()
        self.assertEqual(total_candidate_created.count(),self.total_obj_should_create)
    
    def test_result(self):
        for i in range(0,self.total_obj_should_create):
            result_id =random.randint(0,1000000)
            username = Candidate.objects.create(username = fake.user_name() , name = fake.name(), password = fake.password())
            attempt = random.randint(0,100)
            right = random.randint(0,100)
            wrong = random.randint(0,100)
            points = random.randint(0,100)/10
            result =  Result.objects.create(username=username,
                                            result_id = result_id,
                                            attempt = attempt,
                                            right = right,
                                            wrong = wrong,
                                            points = points
                                            )
            self.assertEqual(result.username,username )
            self.assertEqual(result.result_id,result_id)
        print("second")
        total_result_created = Result.objects.all()
        self.assertEqual(total_result_created.count(),self.total_obj_should_create)
    
    def generate_unique_code():
        length = 6
        while True:
            code= ''.join(random.choices(string.ascii_uppercase,k=length))
            if TestPaperSet.objects.filter(code=code).count()==0:
                break
        return code

    def test_paper_set(self):
        for i in range(0,self.total_obj_should_create):
            test_paper_id = random.randint(0,100000)
            code = generate_unique_code()
            test_paper_name = fake.name()
            total_question = random.randint(0,1000)
            created_by = fake.name()
            start_date = datetime.now().date()
            start_time = datetime.now().time()
            end_date = datetime.now().date()
            end_time = datetime.now().time()
            paper_set = TestPaperSet.objects.create(
                test_paper_id = test_paper_id,
                code = code,
                test_paper_name = test_paper_name,
                total_question = total_question,
                created_by = created_by,
                start_date  = start_date,
                start_time =  start_time,
                end_date = end_date,
                end_time = end_time
            )
            self.paper_set_list.append(paper_set)       
            self.assertEqual(paper_set.test_paper_id,test_paper_id )
            self.assertEqual(paper_set.code , code)
        print("third")
        total_paper_set_created = TestPaperSet.objects.all()
        self.assertEqual(total_paper_set_created.count(),self.total_obj_should_create)

    
    def test_question_set(self):
        for i in range(0 , self.total_obj_should_create):
            test_paper_id = random.randint(0,100000)
            code = generate_unique_code()
            test_paper_name = fake.name()
            total_question = random.randint(0,1000)
            created_by = fake.name()
            start_date = datetime.now().date()
            start_time = datetime.now().time()
            end_date = datetime.now().date()
            end_time = datetime.now().time()
            paper_set = TestPaperSet.objects.create(
                test_paper_id = test_paper_id,
                code = code,
                test_paper_name = test_paper_name,
                total_question = total_question,
                created_by = created_by,
                start_date  = start_date,
                start_time =  start_time,
                end_date = end_date,
                end_time = end_time
            )
            question_set_id = random.randint(0,100000)
            test_paper_id  = paper_set
            question_id = random.randint(0,100000)
            question_set = QuestionSet.objects.create(
                question_set_id = question_set_id,
                test_paper_id = test_paper_id,
                question_id  = question_id
            )
            self.assertEqual(question_set.test_paper_id , test_paper_id)
            self.assertEqual(question_set.test_paper_id, test_paper_id)
            self.assertEqual(question_set.question_id , question_id)
        
        total_question_set  = QuestionSet.objects.all()
        self.assertEqual(total_question_set.count(),self.total_obj_should_create)
        pass
    
