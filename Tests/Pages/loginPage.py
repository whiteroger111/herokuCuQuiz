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

    def enter_first_password(self, password1):
        self.send_Keys_explicit(locators.first_password_id, password1)
        time.sleep(1)

    def enter_second_password(self, password2):
        self.send_Keys_explicit(locators.second_password_id, password2)
        time.sleep(1)

    def confirm_login_button(self):
        self.click_on_element_explicit(locators.confirm_login_button_xpath)
        time.sleep(1)

    def register_as_teacher(self):
        self.click_on_element_explicit(locators.im_teacher_register_xpath)

    def confirm_regisration(self):
        self.click_on_element_explicit(locators.confirm_registration_button_xpath)

    def register_as_student(self):
        self.click_on_element_explicit(locators.im_student_register_xpath)

    def click_on_interests1(self):
        self.click_on_element_explicit(locators.interest1_id)

    def click_on_interests3(self):
        self.click_on_element_explicit(locators.interest3_id)

    def click_on_interests4(self):
        self.click_on_element_explicit(locators.interest4_id)


