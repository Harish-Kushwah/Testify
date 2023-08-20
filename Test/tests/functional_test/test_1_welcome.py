from django.test import LiveServerTestCase
from django.urls import reverse,resolve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# Run specific test only
# python manage.py test Test.tests.test_welcome_page
class TestWelcomePage(LiveServerTestCase):

    def setUp(self):
        self.username = 'h'
        self.password = '123'
        self.name = 'Harish'
        self.welcome_page_url = 'http://127.0.0.1:8000/'
        self.driver  = webdriver.Chrome()
       
    def tearDown(self):
        self.driver.close()

    def test_welcome_page(self):
        driver =self.driver
        driver.get(self.welcome_page_url)
        time.sleep(5)
        assert "Welcome to Online Testing System" in driver.title
    
    # when user is not logged  before then user is redirect to login page
    def test_welcome_page_start_link_to_login(self):
        driver = self.driver
        driver.get(self.welcome_page_url)
        time.sleep(5)
        start_test_link = driver.find_element(By.NAME , 'start_link')
        start_test_link.click()

        login_status = driver.find_element(By.XPATH, "//h4[text()='Login']").is_displayed()
        time.sleep(5)
        self.assertEquals(login_status,True)
    

    # when user was already logged before and came on welcome page and after 
    # that user is redirect to home page
    def test_welcome_page_start_link_to_home(self):
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
        if login_status:
            driver.get(self.welcome_page_url)
            time.sleep(5)
            start_test_link = driver.find_element(By.NAME , 'start_link')
            time.sleep(2)
            start_test_link.click()
            time.sleep(5)
            home_status = driver.find_element(By.XPATH, "//div[@class='home-page']").is_displayed()
            self.assertEquals(home_status,True)
            time.sleep(5)
    
    def test_know_more_btn(self):
        driver = self.driver
        driver.get(self.welcome_page_url)
        time.sleep(5)
        know_more_link = driver.find_element(By.NAME , 'know_more_link')
        know_more_link.click()

        about_status = driver.find_element(By.ID,'about').is_displayed()
        time.sleep(3)
        self.assertEqual(about_status , True)

    def test_navbar_signUp_btn(self):
        driver = self.driver
        driver.get(self.welcome_page_url)

        time.sleep(2)
        nav_signUp = driver.find_element(By.NAME , 'nav_signUp')
        nav_signUp.click()
        time.sleep(5)
        signUp_status = driver.find_element(By.XPATH, "//h4[text()='SignUp']").is_displayed()
        time.sleep(3)
        self.assertEquals(signUp_status,True)
        time.sleep(1)
    
    def test_navbar_login_btn(self):
        driver = self.driver
        driver.get(self.welcome_page_url)

        time.sleep(2)
        nav_login  = driver.find_element(By.NAME,'nav_login')
        nav_login.click()
        time.sleep(5)

        login_status = driver.find_element(By.XPATH,"//h4[text()='Login']").is_displayed()
        time.sleep(3)
        self.assertEqual(login_status , True)

    def test_navbar_about_btn(self):
        driver = self.driver
        driver.get(self.welcome_page_url)

        time.sleep(2)
        nav_about  = driver.find_element(By.NAME,'nav_about')
        nav_about.click()
        time.sleep(5)

        about_status = driver.find_element(By.ID,'about').is_displayed()
        time.sleep(3)
        self.assertEqual(about_status , True)

    def test_navbar_contact_btn(self):
        driver = self.driver
        driver.get(self.welcome_page_url)

        time.sleep(2)
        nav_contact  = driver.find_element(By.NAME,'nav_contact')
        nav_contact.click()
        time.sleep(5)

        contact_status = driver.find_element(By.ID,'contact').is_displayed()
        time.sleep(1)
        self.assertEqual(contact_status , True)
