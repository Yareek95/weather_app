import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture()
def setup(browser):
    if browser == "chrome":
        options = Options()
        options.add_argument("--headless")  # Add this line to run Chrome in headless mode
        driver = webdriver.Chrome(options=options)
        print("Launching Chrome browser in headless mode.............")
    elif browser == "firefox":
        # Similar modifications for Firefox if needed
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        print("Launching Firefox browser in headless mode.............")
    else:
        # Similar modifications for IE if needed
        driver = webdriver.Ie()
    return driver

def pytest_addoption(parser):       #This will get the value from CLI / hooks
    parser.addoption("--browser", default="chrome", help="Choose the browser: chrome, firefox, or ie")

@pytest.fixture()
def browser(request):       #This will return the Browser value to setup method
    return request.config.getoption("--browser")

def pytest_configure(config):
    metadata = {
        'Project Name': 'pocket-book',
        'Module Name': 'weather',
        'Tester': 'Yarik'
    }
    config.option.metadata = metadata
