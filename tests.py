import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestLogin():
    def setUp(self):
        pass

    # tests here

    def tearDown(self):
        self.driver.quit() 
        #to be implemented a method to clean the message data base, for testing purposes
