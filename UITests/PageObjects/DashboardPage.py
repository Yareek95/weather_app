from selenium.webdriver.common.by import By


class DashboardPage:
    txt_welcome_xpath = "//h2[contains(text(), 'Welcome')]"
    btn_logout_xpath = "//a[@href='/logout']//button"


    def __init__(self, driver):
        self.driver = driver

    def txt_welcome(self):
        return self.driver.find_element(By.XPATH, self.txt_welcome_xpath).text

    def click_logout(self):
        self.driver.find_element(By.XPATH, self.btn_logout_xpath).click()
