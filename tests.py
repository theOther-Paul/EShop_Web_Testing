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
