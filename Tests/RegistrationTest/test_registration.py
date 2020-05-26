import time
import datetime
from selenium import webdriver
from Tests.Pages.loginPage import LoginPage


class Test_Resgistration:
    driver = webdriver.Chrome(r'C:\Users\white\Desktop\chromedriver_win32\chromedriver.exe')
    def test_registartion(self):
        self.driver.maximize_window()
        self.driver.get('http://127.0.0.1:8000/')
        loginP = LoginPage(self.driver)
        loginP.click_on_registration_button()
        loginP.register_as_student()
        loginP.enter_username("TEST12")
        loginP.enter_first_password("TESTtest123")
        loginP.enter_second_password("TESTtest123")
        loginP.click_on_interests1()
        loginP.click_on_interests3()
        loginP.click_on_interests4()
        loginP.confirm_regisration()