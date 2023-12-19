import time
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from PageObjects.MainPage import MainPage
from PageObjects.LoginPage import LoginPage


class Test_Page_Titles:
    baseURL = "http://localhost:5000/"          #"https://pb-weather-3c6bf6191360.herokuapp.com/"

    @pytest.mark.sanity
    def test_main_title(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        assert self.driver.title == "PB-Notes"
        self.driver.close()
        print("main_title: ")

    @pytest.mark.sanity
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
        print("login_title")