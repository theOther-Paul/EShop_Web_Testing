import random
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os.path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os.path
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class TestUser:
    """
    In this class, we will test everything user related, like the login process (with correct credentials/incorrect credentials),
    user creation process and credentials switching between user to test if the system allows it.
    """

    @pytest.fixture
    def setUp_teardown(self):
        if os.path.exists("geckodriver.log") and os.path.exists("geckodriver.exe"):
            pass
        else:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        self.driver.get("http://localhost/prestashopSite/")
        self.driver.maximize_window()
        yield
        self.driver.quit()

    def test_page(self, setUp_teardown):
        assert self.driver.title == "General Store"

    def test_login(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
        if self.driver.title == "Login":
            self.driver.find_element(By.ID, 'field-email').send_keys('example@domain.com')
            self.driver.find_element(By.ID, 'field-password').send_keys('example123')
            self.driver.find_element(By.ID, 'submit-login').click()
            self.driver.implicitly_wait(2)
            assert "John Doe" in self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').text
        else:
            assert False

    def test_login_wrongPass(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
        if self.driver.title == "Login":
            self.driver.find_element(By.ID, 'field-email').send_keys('example@domain.com')
            self.driver.find_element(By.ID, 'field-password').send_keys('Example123')
            self.driver.find_element(By.ID, 'submit-login').click()
            assert 'Authentication failed' in self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div/section/div/ul/li').text
        else:
            assert False

    def test_login_wrongUser(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
        if self.driver.title == "Login":
            self.driver.find_element(By.ID, 'field-email').send_keys('example@domain.net')
            self.driver.find_element(By.ID, 'field-password').send_keys('example123')
            self.driver.find_element(By.ID, 'submit-login').click()
            assert 'Authentication failed' in self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div/section/div/ul/li').text
        else:
            assert False

    def test_create_user(self, setUp_teardown):
        self.driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
        self.driver.find_element(By.LINK_TEXT, "No account? Create one here").click()
        self.driver.find_element(By.ID, "field-id_gender-2").click()
        self.driver.find_element(By.ID, "field-firstname").click()
        self.driver.find_element(By.ID, "field-firstname").send_keys("Smith")
        self.driver.find_element(By.ID, "field-lastname").click()
        self.driver.find_element(By.ID, "field-lastname").send_keys("Jane")
        self.driver.find_element(By.ID, "field-email").click()
        self.driver.find_element(By.ID, "field-email").send_keys(f"example{random.random()}@domain.net")
        self.driver.find_element(By.ID, "field-password").click()
        self.driver.find_element(By.ID, "field-password").send_keys("GenericPass")
        self.driver.find_element(By.CSS_SELECTOR, ".input-group-btn > .btn").click()
        self.driver.find_element(By.ID, "field-password").click()
        self.driver.find_element(By.NAME, "psgdpr").click()
        self.driver.find_element(By.CSS_SELECTOR, ".form-control-submit").click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.NAME, "customer_privacy").click()
        self.driver.find_element(By.CSS_SELECTOR, ".form-control-submit").click()
        self.driver.find_element(By.ID, "wrapper").click()
        assert "Smith Jane" in self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').text


