from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os.path
from selenium.webdriver.firefox.options import Options as FirefoxOptions


if os.path.exists("geckodriver.log") and os.path.exists("geckodriver.exe"):
    print("found")
else:
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("http://localhost/prestashopSite/login?back=my-account")
print(driver.title)
driver.quit()
