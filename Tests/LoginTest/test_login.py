import time
from selenium import webdriver
from Tests.Pages.loginPage import LoginPage


class Test_Login:
    driver = webdriver.Chrome(r'C:\Users\white\Desktop\chromedriver_win32\chromedriver.exe')

    def test_authorization(self):
        self.driver.maximize_window()
        self.driver.get('http://127.0.0.1:8000/')
        loginP = LoginPage(self.driver)
        loginP.click_on_login_button()

        loginP.enter_username('Nika2')

        loginP.enter_password('ZARNzarn123')

        loginP.confirm_login_button()
