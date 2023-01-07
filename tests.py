import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os.path
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class TestLogin:
    @classmethod
    def setUp(self):
        if os.path.exists("geckodriver.log") and os.path.exists("geckodriver.exe"):
            pass
        else:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        self.driver.get("http://localhost/prestashopSite/")
        self.driver.maximize_window()


    def test_page(self):
        # self.setUp()
        assert self.driver.title == "General Store"
        # self.tearDown()

    # def test_login(self):
    #     self.driver.get('http://localhost/prestashopSite/')

    @classmethod
    def tearDown(self):
        self.driver.quit()
        # to be implemented a method to clean the message data base, for testing purposes

@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium