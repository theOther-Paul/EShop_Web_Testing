import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os.path
import generate_new_users


class TestUser:
    """
    In this class, we will test everything user related, like the login process (with correct credentials/incorrect credentials),
    user creation process and credentials switching between user to test if the system allows it.
    """

    @pytest.fixture
    def setUp_teardown(self):
        if not os.path.exists("geckodriver.exe"):
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        else:
            self.driver = webdriver.Firefox()

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
        generate_new_users.api_connection()
        if "Mr" in generate_new_users.get_gender_title('user_data.json'):
            self.driver.find_element(By.ID, 'field-id_gender-1').click()
        else:
            self.driver.find_element(By.ID, "field-id_gender-2").click()
        self.driver.find_element(By.ID, "field-firstname").click()
        self.driver.find_element(By.ID, "field-firstname").send_keys(f"{generate_new_users.get_first_name('user_data.json')}")
        self.driver.find_element(By.ID, "field-lastname").click()
        self.driver.find_element(By.ID, "field-lastname").send_keys(f"{generate_new_users.get_last_name('user_data.json')}")
        self.driver.find_element(By.ID, "field-email").click()
        self.driver.find_element(By.ID, "field-email").send_keys(f"{generate_new_users.get_email('user_data.json')}")
        self.driver.find_element(By.ID, "field-password").click()
        self.driver.find_element(By.ID, "field-password").send_keys(f"{generate_new_users.get_password('user_data.json')}")
        self.driver.find_element(By.CSS_SELECTOR, ".input-group-btn > .btn").click()
        self.driver.find_element(By.ID, "field-password").click()
        self.driver.find_element(By.NAME, "psgdpr").click()
        self.driver.find_element(By.CSS_SELECTOR, ".form-control-submit").click()
        self.driver.find_element(By.NAME, "customer_privacy").click()
        self.driver.find_element(By.CSS_SELECTOR, ".form-control-submit").click()
        self.driver.find_element(By.ID, "wrapper").click()
        try:
            assert f"{generate_new_users.get_first_last_name('user_data.json')}" in self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').text
        except AssertionError:
            generate_new_users.dump_user_data()
            self.driver.get_full_page_screenshot_as_file(f"failed_tests_shots/create_user_{generate_new_users.get_first_last_name('user_data.json')}.png")
            assert False
        finally:
            generate_new_users.drop_user_data('user_data.json')

    def test_logout_user(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
        if self.driver.title == "Login":
            self.driver.find_element(By.ID, 'field-email').send_keys('example@domain.com')
            self.driver.find_element(By.ID, 'field-password').send_keys('example123')
            self.driver.find_element(By.ID, 'submit-login').click()
            account_name = self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span')
        if "John Doe" in account_name.text:
            self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[1]').click()
            assert self.driver.title == "Login"
        else:
            assert False


class TestProduct:
    """
    in this class will be tested the basic functionality of the store: adding products in a card, getting a correct total, customizing a product, deleting it from a cart, checking if a product out of stock could be added to a cart,
    adding a product to favourites, etc.
    """

    @pytest.fixture
    def setUp_teardown(self):
        if not os.path.exists("geckodriver.exe"):
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        else:
            self.driver = webdriver.Firefox()

        self.driver.get("http://localhost/prestashopSite/")
        self.driver.maximize_window()
        yield
        self.driver.quit()

    def add_to_cart(self, setUp_teardown):
        pass
