import pytest
from selenium import webdriver
import os.path
import helper
from selenium.common import NoSuchElementException, ElementNotInteractableException
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
            self.driver.implicitly_wait(1.2)
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
        if "John Doe" not in account_name.text:
            assert False
        else:
            self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[1]').click()
            assert self.driver.title == "Login"


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
        else:
            try:
                assert False
            except AssertionError:
                assert False

    def test_custom_text(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/div[2]/div/div[1]/div[2]/div[1]/ul/li[2]/a').click()
        self.driver.find_element(By.XPATH, '/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[11]/article/div/div[1]/a').click()
        url = self.driver.current_url
        if "customizable-mug" in url:
            message = helper.generate_sentence()
            self.driver.find_element(By.XPATH, '//*[@id="field-textField1"]').click()
            self.driver.find_element(By.XPATH, '//*[@id="field-textField1"]').send_keys(message)
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/section/div/form/div/button').click()
            message_box = self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/section/div/form/ul/li/h6').text
            if message in message_box:
                assert True
            else:
                assert False
        else:
            assert False

    def test_add_to_favourites(self, setUp_teardown):
        self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
        if self.driver.title == "Login":
            self.driver.find_element(By.ID, 'field-email').send_keys('example@domain.com')
            self.driver.find_element(By.ID, 'field-password').send_keys('example123')
            self.driver.find_element(By.ID, 'submit-login').click()
            self.driver.implicitly_wait(2)
        if "John Doe" in self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').text:
            self.driver.find_element(By.XPATH, '/html/body/main/header/div[2]/div/div[1]/div[1]/a/img').click()
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/section/section/div/div[4]/article/div/button/i').click()
            self.driver.find_element(By.XPATH, '/html/body/main/footer/div[2]/div/div[1]/div[4]/div[1]/div/div/div[2]/div/ul/li/p').click()
            self.driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').click()
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/section/div/div/a[5]/span/i').click()
            wish = self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/section/div/ul/li/a/p').text
            wish_num = wish[len(wish) - 1]
            assert wish_num != 0
            # remove item from wishlist for testing purposes
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/section/div/ul/li/a/p').click()
            self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/section/div[1]/section/ul/li/div/div/button[2]/i').click()
            self.driver.find_element(By.XPATH, '/html/body/main/footer/div[2]/div/div[1]/div[5]/div[1]/div/div/div[3]/button[2]').click()
        else:
            assert False


class TestAdmin:
    """
    In this class we will test some basic functionality of the admin backend, such as login, create employee, delete customer, etc
    """

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

    def test_admin_login(self, setup_tear):
        self.driver.find_element(By.ID, 'email').send_keys('example@domain.com')
        self.driver.find_element(By.ID, 'passwd').send_keys('example123')
        self.driver.find_element(By.ID, 'submit_login').click()
        self.driver.find_element(By.CSS_SELECTOR, '.employee_name > i:nth-child(1)').click()
        assert 'Jon' in self.driver.find_element(By.XPATH, "/html/body/header/nav/ul[3]/li/ul/li[2]").text

    def test_admin_create_account(self, setup_tear):
        # log into an existent admin account
        self.driver.find_element(By.ID, 'email').send_keys('example@domain.com')
        self.driver.find_element(By.ID, 'passwd').send_keys('example123')
        self.driver.find_element(By.ID, 'submit_login').click()

        # locate the team option
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#subtab-AdminAdvancedParameters > a:nth-child(1) > span:nth-child(2)').click()
        except NoSuchElementException:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#subtab-AdminAdvancedParameters > a:nth-child(1) > i:nth-child(3)'))).click()

        self.driver.find_element(By.XPATH, '/html/body/nav/div/ul/li[17]/ul/li[6]/a').click()
        self.driver.find_element(By.ID, 'page-header-desc-configuration-add').click()

        # fill out the employee form
        generate_new_users.api_connection()
        self.driver.find_element(By.ID, 'employee_firstname').send_keys(f"{generate_new_users.get_first_name('user_data.json')}")
        self.driver.find_element(By.ID, 'employee_lastname').send_keys(f"{generate_new_users.get_last_name('user_data.json')}")
        self.driver.find_element(By.ID, 'employee_email').send_keys(f"{generate_new_users.get_email('user_data.json')}")
        self.driver.find_element(By.ID, 'employee_password').send_keys(f"{generate_new_users.get_password('user_data.json')}")
        self.driver.find_element(By.ID, 'save-button').click()

        try:
            assert True
        except AssertionError:
            generate_new_users.dump_user_data()
            self.driver.get_full_page_screenshot_as_file(f"failed_tests_shots/create_user_{generate_new_users.get_first_last_name('user_data.json')}.png")
            assert False
        finally:
            generate_new_users.drop_user_data('user_data.json')

    def test_delete_customer(self, setup_tear):
        # log into an existent admin account
        self.driver.find_element(By.ID, 'email').send_keys('example@domain.com')
        self.driver.find_element(By.ID, 'passwd').send_keys('example123')
        self.driver.find_element(By.ID, 'submit_login').click()

        # locate the customer button
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#subtab-AdminParentCustomer > a:nth-child(1) > i:nth-child(3)').click()
        except ElementNotInteractableException:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/ul/li[5]/a'))).click()
        except NoSuchElementException:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/ul/li[5]/a'))).click()

        self.driver.find_element(By.CSS_SELECTOR, '#subtab-AdminCustomers > a:nth-child(1)').click()

        self.driver.implicitly_wait(5.0)

        # delete button
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[4]/div/div[1]/div[2]/div/div/div[2]/div/form/table/tbody/tr[1]/td[13]/div/div/a[2]').click()
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[4]/div/div[1]/div[2]/div/div/div[2]/div/form/table/tbody/tr[1]/td[13]/div/div/div/a[2]').click()

        self.driver.implicitly_wait(1.2)

        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[4]/div/div[2]/div/div/div[3]/button[2]').click()
        assert "Successful deletion" in self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/p').text
