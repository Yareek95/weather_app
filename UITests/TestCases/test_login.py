import time
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException

from PageObjects.MainPage import MainPage
from PageObjects.LoginPage import LoginPage
from PageObjects.DashboardPage import DashboardPage


class Test_Login:
    baseURL = "https://pb-weather-3c6bf6191360.herokuapp.com/"          #"http://localhost:5000/"

    @pytest.mark.regression
    @pytest.mark.login
    def test_valid_logins(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)

        self.mp = MainPage(self.driver)
        self.lp = LoginPage(self.driver)
        self.dp = DashboardPage(self.driver)

        self.mp.click_login_btn()
        self.lp.input_username("q")             # q,w,e is valid, pass: 1
        self.lp.input_password("1")
        self.lp.click_submit()

        assert self.dp.txt_welcome() == "Welcome, Q!"
        self.dp.click_logout()
        self.driver.close()
        print("valid_logins: success")

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_invalid_logins(self, setup):
        pytest.skip("Not ready, skipping...")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

        self.mp = MainPage(self.driver)
        self.lp = LoginPage(self.driver)

        self.lp.input_username("q")             # q,w,e is valid, pass: 1
        self.lp.input_password("1")
        self.lp.click_submit()

        assert self.dp.txt_welcome() == ""
        self.driver.close()
        print("invalid_logins: success")