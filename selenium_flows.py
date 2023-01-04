from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


# only for experimentation. Will be removed when the project is complete
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get("http://localhost/prestashopSite/")
assert "General Store" in driver.title
