from selenium.webdriver.common.by import By


class LoginPage:
    btn_registration_xpath = "//a[@href='/register']//button"
    btn_info_xpath = "//a[@href='/about']//button"
    btn_main_xpath = "//a[@href='/']//button"
    input_username_id = "username"
    input_password_id = "password"
    btn_submit_xpath = "//button[@type='submit']"

    def __init__(self, driver):
        self.driver = driver

    def input_username(self, username):
        self.driver.find_element(By.ID, self.input_username_id).send_keys(username)

    def input_password(self, password):
        self.driver.find_element(By.ID, self.input_password_id).send_keys(password)

    def click_submit(self):
        self.driver.find_element(By.XPATH, self.btn_submit_xpath).click()