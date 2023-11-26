from selenium.webdriver.common.by import By


class MainPage:
    input_city_id = "user_input"
    btn_get_weather_xpath = "//button[normalize-space()='Get Weather']"
    txt_location_xpath = "//h2"
    txt_main_xpath = "//h1"

    def __init__(self, driver):
        self.driver = driver

    def title(self):
        title = self.driver.title
        return title

    def txt_main(self):
        return self.driver.find_element(By.XPATH, self.txt_main_xpath).text

    def input_town_name(self, city_name):
        self.driver.find_element(By.ID, self.input_city_id).send_keys(city_name)

    def click_get_weather(self):
        self.driver.find_element(By.XPATH, self.btn_get_weather_xpath).click()

    def location_displayed(self):
        return self.driver.find_element(By.XPATH, self.txt_location_xpath).is_displayed()
