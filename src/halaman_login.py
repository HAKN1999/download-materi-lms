from time import sleep
from helper.selenium_driver import SeleniumDriver


class HalamanLogin(SeleniumDriver):
    base_URL = "https://camp.ruangguru.com/"

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.driver = driver
        self.driver.get(self.base_URL)

    # locators
    _email_xpath = "//input[@type='text']"
    _password_xpath = "//input[@type='password']"
    _next_button = "//*[text()='SELANJUTNYA']"
    _login_button = "//*[text()='MASUK']"
    _account_xpath = "//p[@class='css-1315gl']"

    def enter_email(self, email):
        self.waitForElement(self._email_xpath, "xpath")
        self.sendKeys(email, self._email_xpath, "xpath")

    def enter_password(self, password):
        self.waitForElement(self._password_xpath, "xpath")
        self.sendKeys(password, self._password_xpath, "xpath")

    def click_next_button(self):
        self.elementClick(self._next_button, "xpath")

    def click_login_button(self):
        self.elementClick(self._login_button, "xpath")

    def login(self, email, password):
        self.enter_email(email)
        self.click_next_button()
        self.enter_password(password)
        self.click_login_button()

    def verify_login_successful(self):
        self.waitForElement(self._account_xpath, "xpath")
        result, element = self.isElementPresent(self._account_xpath, "xpath")
        print()
        print("=" * 10)
        if result:
            account_name = element.text
            print("Login berhasil")
            print(f"Hi.., {account_name}")
        else:
            exit("Login gagal")
