from behave import *
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import os


@given('the user enters the credentials for the shop')
def sep_impl(context):
    if not os.path.exists("geckodriver.exe"):
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )
    else:
        driver = webdriver.Firefox()

    driver.get("http://localhost/prestashopSite/")
    driver.maximize_window()
    driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a').click()
    if driver.title == "Login":
        driver.find_element(By.ID, 'field-email').send_keys('example@domain.com')
        driver.find_element(By.ID, 'field-password').send_keys('example123')

    driver.find_element(By.ID, 'submit-login').click()


@then('they should see their name in the top of the page')
def step_impl(context):
    driver = webdriver.Firefox()
    assert "John Doe" in driver.find_element(By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span').text
