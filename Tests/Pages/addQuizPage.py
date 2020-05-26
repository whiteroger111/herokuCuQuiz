from Tests import locators
from Tests.utility import Utility
import time


class AddQuizPage(Utility):
    def __init__(self, driver):
        super().__init__(driver)

    def go_to_quiz_add_page(self):
        self.click_on_element_explicit(locators.go_to_add_quiz_page_button_xpath)

    def enter_quiz_name(self,quizName):
        self.send_Keys_explicit(locators.quiz_name_input_id,quizName)

    def pick_subject(self):
        self.click_on_element_explicit(locators.quiz_subject_dropdown)
        self.click_on_element_explicit(locators.quiz_subject_option)
        time.sleep(1)

    def save_quiz_name_and_subject(self):
        self.click_on_element_explicit(locators.save_quiz_button_xpath)

    def enter_question_text(self, text):
        self.send_Keys_explicit(locators.question_text_id, text)

    def click_on_add_question_text_button(self):
        self.click_on_element_explicit(locators.add_question_text_button)

    def goto_add_question_page(self):
        self.click_on_element_explicit(locators.goto_add_qustion_button_xpath)

    def choose_correct_anwser(self):
        self.click_on_element_explicit(locators.question_correct_anwser_first)

    def add_answers_all(self):
        self.click_on_element_explicit(locators.add_answers_button_xpath)



