import time
import pytest
import allure
from selenium import webdriver
from selenium.common import NoSuchElementException
from PageObjects.MainPage import MainPage
from PageObjects.LoginPage import LoginPage


class Test_Page_Titles:
    baseURL = "https://pb-weather-3c6bf6191360.herokuapp.com/"          #"https://pb-weather-3c6bf6191360.herokuapp.com/"

    @allure.severity(allure.severity_level.NORMAL)
    def test_main_title(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(1)
        assert self.driver.title == "PB-Notes"
        self.driver.close()

    @allure.severity(allure.severity_level.NORMAL)
    def test_login_title(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.mp = MainPage(self.driver)
        self.lp = LoginPage(self.driver)

        self.mp.click_login_btn()
        assert self.driver.title == "Login"
        self.driver.close()