import time
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from PageObjects.MainPage import MainPage


class Test_weather_location:
    baseURL = "http://localhost:5000/"          #"https://pb-weather-3c6bf6191360.herokuapp.com/"

    def test_main_txt(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.mp = MainPage(self.driver)
        assert self.mp.txt_main() == "Weather App"
        self.driver.close()

    def test_main_location(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.mp = MainPage(self.driver)
        self.mp.input_town_name("Chicago")
        self.mp.click_get_weather()
        assert self.mp.location_displayed()
        self.driver.quit()


    def test_title_txt(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.mp = MainPage(self.driver)
        assert self.mp.title() == "Weather App"
        self.driver.quit()
