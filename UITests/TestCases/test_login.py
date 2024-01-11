import time
import pytest
import allure
from selenium import webdriver
from selenium.common import NoSuchElementException

from utilities import XLUtils
from PageObjects.MainPage import MainPage
from PageObjects.LoginPage import LoginPage
from PageObjects.DashboardPage import DashboardPage


class Test_Login:
    baseURL = "https://pb-weather-3c6bf6191360.herokuapp.com/"
    path_LoginData = ".//TestData/LoginData.xlsx"

    @pytest.mark.login
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_logins(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)

        self.mp = MainPage(self.driver)
        self.lp = LoginPage(self.driver)
        self.dp = DashboardPage(self.driver)

        self.rows = XLUtils.getRowCount(self.path_LoginData, "Positive")
        for r in range(2, self.rows + 1):
            self.username = XLUtils.readData(self.path_LoginData, "Positive", r, 1)
            self.password = XLUtils.readData(self.path_LoginData, "Positive", r, 2)

            self.mp.click_login_btn()
            self.lp.input_username(self.username)             # q,w,e is valid, pass: 1
            self.lp.input_password(self.password)
            self.lp.click_submit()
            assert self.dp.txt_welcome().lower() == f"welcome, {self.username}!"
            self.dp.click_logout()

        self.driver.close()

    @pytest.mark.login
    @allure.severity(allure.severity_level.BLOCKER)
    def test_invalid_logins(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

        self.mp = MainPage(self.driver)
        self.lp = LoginPage(self.driver)
        self.dp = DashboardPage(self.driver)

        self.rows = XLUtils.getRowCount(self.path_LoginData, "Negative")

        self.mp.click_login_btn()

        for r in range(2, self.rows + 1):
            self.username = XLUtils.readData(self.path_LoginData, "Negative", r, 1)
            self.password = XLUtils.readData(self.path_LoginData, "Negative", r, 2)
            self.exp_error_msg = XLUtils.readData(self.path_LoginData, "Negative", r, 3)

            self.lp.input_username(self.username)  # q,w,e is valid, pass: 1
            self.lp.input_password(self.password)
            self.lp.click_submit()

            assert self.lp.error_msg_txt() == self.exp_error_msg
        self.driver.close()
