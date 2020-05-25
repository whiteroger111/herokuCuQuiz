from Tests import locators
from Tests.utility import Utility
import time


class LoginPage(Utility):
    def __init__(self, driver):
        super().__init__(driver)

    def click_on_login_button(self):
        self.click_on_element_explicit(locators.enter_login_button_xpath)
        time.sleep(1)

    def click_on_registration_button(self):
        self.click_on_element_explicit(locators.enter_registration_button_xpath)
        time.sleep(1)

    def enter_username(self, username):
        self.send_Keys_explicit(locators.login_form_username_input_id, username)
        time.sleep(1)

    def enter_password(self, password):
        self.send_Keys_explicit(locators.login_form_password_input_id, password)
        time.sleep(1)

    def confirm_login_button(self):
        self.click_on_element_explicit(locators.confirm_login_button_xpath)
        time.sleep(1)