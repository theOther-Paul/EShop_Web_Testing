import pytest
from selenium import webdriver
import os.path

from selenium.common import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            assert f"{generate_new_users.get_first_last_name('user_data.json')}" in self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div['
                                                                                                                       '1]/div/a[2]/span').text
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


class TestProduct(TestUser):
    """
    in this class will be tested the basic functionality of the store: adding products in a card, getting a correct total, customizing a product, deleting it from a cart,
    checking if a product out of stock could be added to a cart,
    adding a product to favourites, etc.
    """

    def test_add_to_cart(self, setUp_teardown):
        self.driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/section/section/div/div[1]/article/div/div[1]/a/img").click()
        self.driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button").click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/a"))).click()
        no_item = self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]').text
        assert no_item[0] != 0

    def test_remove_from_cart(self, setUp_teardown):
        self.driver.find_element(By.CSS_SELECTOR, ".js-product:nth-child(1) img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".touchspin-up").click()
        self.driver.find_element(By.CSS_SELECTOR, ".add-to-cart").click()

        # checkout button
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/a'))).click()

        self.driver.find_element(By.CSS_SELECTOR, ".remove-from-cart > .material-icons").click()
        try:
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div/div[2]/div[1]/div[2]/div/a').is_enabled()
            assert True
        except NoSuchElementException:
            assert False

    def test_dif_color(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/section/section/div/div[1]/article/div/div[1]/a/img').click()
        if self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[1]/div[2]/ul/li[2]/label/input').click():
            assert True


class TestAdmin:
    @pytest.fixture()
    def setup_tear(self):
        if not os.path.exists("geckodriver.exe"):
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        else:
            self.driver = webdriver.Firefox()

        self.driver.get("http://localhost/prestashopSite/admin616n4hbcx")
        self.driver.maximize_window()
        yield
        self.driver.quit()

    def test_admin_login(self):
        pass

    def test_admin_create_account(self):
        pass

    def test_delete_user(self):
        pass
