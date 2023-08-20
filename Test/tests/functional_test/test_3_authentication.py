from django.test import LiveServerTestCase
from faker import Faker
from Test.models import *
from django.urls import reverse,resolve
from Test.views import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Run specific test only
# python manage.py test Test.tests.functional_test.TestLoginPage
    
class TestLoginPage(LiveServerTestCase):
    def __init__(self):
        pass

    def setUp(self):
        self.username = 'h'
        self.password = '123'
        self.name = 'Harish'

        self.driver  = webdriver.Chrome()
       
    def tearDown(self):
        self.driver.close()

    def test_login_page(self):
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
        
        time.sleep(5)
        login_status = driver.find_element(By.XPATH, "//div[@class='home-page']").is_displayed()
        
        self.assertEquals(login_status,True)


class TestSignUpPage(LiveServerTestCase):
    def setUp(self):
        fake = Faker()
        self.username = fake.user_name()
        self.password = fake.password()
        self.name = fake.name()

        self.driver  = webdriver.Chrome()
       
    def tearDown(self):
        self.driver.close()

    def test_signUp_page(self):
        driver =self.driver
        driver.get('http://127.0.0.1:8000/Test/registrationform')

        name = driver.find_element(By.ID ,'name')
        user_name = driver.find_element(By.ID,'username')
        password = driver.find_element(By.NAME,'password')
        submit = driver.find_element(By.NAME,'btn')

        name.send_keys(self.name)
        user_name.send_keys(self.username)
        password.send_keys(self.password)
        submit.send_keys(Keys.RETURN)
        
        time.sleep(5)
        signUp_status = driver.find_element(By.ID, "//h4[text()='Login']").is_displayed()
        time.sleep(5)

        self.assertEquals(signUp_status,True)
