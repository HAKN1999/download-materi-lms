from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import utilities.custom_logger as cl
from traceback import print_stack
import logging


class SeleniumDriver:
    log = cl.customLogger(logLevel=logging.INFO)

    def __init__(self, driver):
        self.driver = driver

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            print("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info(
                "Element Found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        except:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        return element

    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info(
                "Clicked on element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
        except:
            self.log.info(
                "Cannot click on the element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
            # print_stack()

    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info(
                "Sent data on element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
        except:
            self.log.info(
                "Cannot send data on the element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
            # print_stack()

    def isElementPresent(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True, element
            else:
                self.log.info("Element not found")
                return False, element
        except:
            self.log.info("Element not found")
            return False, element

    def elementPresence(self, locator, byType):
        elementList = None
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True, elementList
            else:
                self.log.info("Element not found")
                return False, elementList
        except:
            self.log.info("Element not found")
            return False, elementList

    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.10):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info(
                "Waiting for maximum :: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                self.driver,
                10,
                poll_frequency=1,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            # print_stack()
        return element

    def waitForElementPresent(
        self, locator, locatorType="id", timeout=10, pollFrequency=0.10
    ):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info(
                "Waiting for maximum :: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                self.driver,
                10,
                poll_frequency=1,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            # print_stack()
        return element

    def waitForElementPresentVisibility(
        self, locator, locatorType="id", timeout=10, pollFrequency=0.10
    ):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info(
                "Waiting for maximum :: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                self.driver,
                10,
                poll_frequency=1,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element appeared on the web page")
        except Exception as e:
            self.log.info("Element not appeared on the web page")
            # print_stack()
        return element
