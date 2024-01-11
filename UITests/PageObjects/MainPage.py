from selenium.webdriver.common.by import By


class MainPage:
    btn_login_xpath = "//button[normalize-space()='Login']"
    btn_registration_xpath = "//button[normalize-space()='Registration']"
    btn_info_xpath = "//button[normalize-space()='Info']"
    txt_main_xpath = "//h1"

    def __init__(self, driver):
        self.driver = driver

    def click_login_btn(self):
        self.driver.find_element(By.XPATH, self.btn_login_xpath).click()
