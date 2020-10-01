import os
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pyperclip


class Utils:
    def __init__(self):
        self.chrome_driver_path = os.getcwd() + "/drivers/chromedriver"
        self.firefox_driver_path = os.getcwd() + "/drivers/geckodriver"
        self.naver_vibe_url = "https://vibe.naver.com/today"

    def get_chrome_driver(self):
        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.implicitly_wait(3)
        return driver

    def get_firefox_driver(self):
        driver = webdriver.Firefox(executable_path=self.firefox_driver_path)
        driver.implicitly_wait(3)
        return driver

    def shutdown(self, msg, driver=None):
        if driver is not None:
            driver.quit()
        print(msg)

    def vibe_login(self, driver, id, pw):
        result = True
        try:
            driver.get(self.naver_vibe_url)
            driver.find_element_by_class_name("ico_close").click()
            sleep(1)
            driver.find_element_by_class_name("link_login").click()
            sleep(1)

            pyperclip.copy(id)
            id_element = driver.find_element_by_name("id")
            id_element.click()
            sleep(1)
            id_element.send_keys(Keys.COMMAND, "v")
            sleep(1)

            pyperclip.copy(pw)
            id_element = driver.find_element_by_name("pw")
            id_element.click()
            sleep(1)
            id_element.send_keys(Keys.COMMAND, "v")
            sleep(1)

            driver.find_element_by_id("log.login").click()
            sleep(1)
            driver.find_element_by_id("new.save").click()
            sleep(1)
        except NoSuchElementException:
            result = False
            self.shutdown(msg="Failed to VIBE Login", driver=driver)
        finally:
            return result
