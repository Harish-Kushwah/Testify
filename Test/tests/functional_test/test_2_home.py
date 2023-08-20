from django.test import LiveServerTestCase
from faker import Faker
from Test.models import *
from django.urls import reverse,resolve
from Test.views import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TestHomePage(LiveServerTestCase):
    def setUp(self):
        self.username = 'h'
        self.password = '123'
        self.name = 'Harish'
        self.home_page_url = 'http://127.0.0.1:8000/Test/home'
        self.driver  = webdriver.Chrome()
        self.login_status  = self.loginUser()
       
    
    def tearDown(self):
        self.driver.close()
    
    def loginUser(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/Test/login')

        user_name = driver.find_element(By.NAME,'username')
        password = driver.find_element(By.NAME,'password')
        submit = driver.find_element(By.NAME,'btn')
        
        user_name.clear()
        user_name.send_keys(self.username)
        password.clear() 
        password.send_keys(self.password)
        submit.send_keys(Keys.RETURN)
        
        time.sleep(1)
        login_status = driver.find_element(By.XPATH, "//div[@class='home-page']").is_displayed()
        if login_status:
            return login_status


    def test_compete_btn(self):
        if self.login_status :
            driver = self.driver
            time.sleep(2)
            nav_compete = driver.find_element(By.NAME , 'nav_compete')
            nav_compete.click()
            time.sleep(2)
            compete_status = driver.find_element(By.NAME, "all_test_head").is_displayed()
            self.assertEquals(compete_status,True)
            time.sleep(2)
        else:
            print("unable to login user")
    
    def test_createTest_paper(self):
        if self.login_status:
            name = 'MATH'
            total_question_num = 2
            driver = self.driver
            time.sleep(3)
            topic_name = driver.find_element(By.NAME,'topic_name')
            total_question = driver.find_element(By.NAME,'total_que')
            submit = driver.find_element(By.NAME,'custome_test_paper_btn')
            
            topic_name.clear()
            topic_name.send_keys(name)
            total_question.clear() 
            total_question.send_keys(total_question_num)
            submit.send_keys(Keys.RETURN)
            time.sleep(5)
            exam_status = driver.find_element(By.XPATH, "//h2[text()='Exam Section']").is_displayed()
            self.assertEquals(exam_status,True)
            time.sleep(3)
        else:
            print("unable to login user")
    
    def test_start_testPaper_set(self):
        if self.login_status:
            code = 'ESAZTE'
            driver = self.driver
            time.sleep(3)
            code_input = driver.find_element(By.NAME , 'code')
            submit = driver.find_element(By.NAME,'paper_set_btn')
            code_input.clear() 
            code_input.send_keys(code)
            submit.send_keys(Keys.RETURN)
            time.sleep(5)
            exam_status = driver.find_element(By.XPATH, "//h2[text()='Exam Section']").is_displayed()
            time.sleep(3)
            self.assertEquals(exam_status,True)
        else:
            print("unable to login user")
    
    def test_set_testPaper(self):
        if self.login_status:
            driver = self.driver
            time.sleep(3)
            
            set_testPaper_link = driver.find_element(By.NAME , 'set_test_paper')
            set_testPaper_link.click()

            set_testPaper_status = driver.find_element(By.ID,'test_paper_head').is_displayed()
            time.sleep(3)
            self.assertEqual(set_testPaper_status , True)
        else:
            print("unable to login user")

    def test_NIMCET_link(self):
        if self.login_status:
            driver = self.driver
            time.sleep(3)
            
            NIMCET_link = driver.find_element(By.NAME , 'NIMCET_link')
            NIMCET_link.click()

            exam_status = driver.find_element(By.XPATH, "//h2[text()='Exam Section']").is_displayed()
            time.sleep(3)
            self.assertEquals(exam_status,True)
        else:
            print("unable to login user")

    def test_paper_analysis(self):
        if self.login_status:
            driver = self.driver
            time.sleep(3)
            
            paper_analysis = driver.find_element(By.NAME , 'paper_analysis')
            paper_analysis.click()

            report_card_header = driver.find_element(By.ID, "report_card_header").is_displayed()
            time.sleep(3)
            self.assertEquals(report_card_header,True)
        else:
            print("unable to login user")
