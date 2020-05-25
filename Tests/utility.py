from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


import pytest




class Utility:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locatorTuple, timeout=10):
        element = None
        locatorType = locatorTuple[0]
        locator = locatorTuple[1]
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((locatorType, locator)))
            return element
        except TimeoutException:
            print(TimeoutException)

    def click_on_element_explicit(self, locatorTuple, timeout=10):
        locatorType = locatorTuple[0]
        locator = locatorTuple[1]
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable((locatorType, locator))).click()
        except TimeoutException:
            print(TimeoutException)

    def send_Keys_explicit(self, locatorTuple, data, timeout=10):
        locatorType = locatorTuple[0]
        locator = locatorTuple[1]
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable((locatorType, locator))).send_keys(data)
        except TimeoutException:
            print(TimeoutException.__repr__())







