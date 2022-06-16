from time import sleep
from lxml import html
import os

from helper.selenium_driver import SeleniumDriver
from utilities.checkpoint import CheckPoint
from src.halaman_kedua import HalamanKedua


class HalamanUtama(SeleniumDriver):
    base_URL = "https://camp.ruangguru.com/me/learning-plan/flexible-course"
    fnama_checkpoint = "materi_checkpoint.txt"

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.driver = driver
        self.Checkpoint = CheckPoint()
        self.HalamanKedua = HalamanKedua(driver)

    # locators
    _scroll_halaman_xpath = "css-z01v1j"
    _scroll_materi_xpath = "css-1qeeb8j"
    _section_materi_xpath = "//div[@class='css-vufj71']"
    _title_materi_xpath = "//*[@class='css-bzrok0']"
    _informasi_xpath = "//p[@class='css-dvz6pl']"

    def scroll_materi(self):
        script = "document.getElementsByClassName('css-1qeeb8j')[0].scrollBy(0, 999999)"
        self.driver.execute_script(script)

    def scroll_halaman(self):
        self.elementPresence(self._scroll_halaman_xpath, "xpath")
        sleep(3)
        script = "document.getElementsByClassName('css-z01v1j')[0].scrollBy(0, 999999)"
        self.driver.execute_script(script)

    def click_materi(self, nama_materi):
        judul_materi_xpath = f"//*[text()='{nama_materi}']"
        element = self.waitForElement(judul_materi_xpath, "xpath")
        element.click()

        self.elementPresence(self._informasi_xpath, "xpath")
        sleep(2)

    def ambil_judul_materi(self, list_element_materi):
        judul_materi_xpath = "//*[@class='css-bzrok0']"
        list_judul_materi = []
        for element in list_element_materi:
            souce_lxml = html.fromstring(str(element.get_attribute("innerHTML")))
            element_text = souce_lxml.xpath(judul_materi_xpath)[0].text

            list_judul_materi.append(element_text)
        return list_judul_materi

    def ambil_list_materi(self):
        self.driver.get(self.base_URL)
        self.scroll_halaman()

        for _ in range(100):
            self.scroll_materi()
            sleep(0.02)

        self.waitForElementPresent(self._section_materi_xpath, "xpath")
        is_element_presence, elementList = self.elementPresence(self._section_materi_xpath, "xpath")

        if is_element_presence:
            list_judul_materi = self.ambil_judul_materi(elementList)
            for judul_materi in list_judul_materi:
                is_downloaded, status = self.Checkpoint.baca_file_checkpoint(self.fnama_checkpoint, judul_materi)

                if is_downloaded:
                    continue

                else:
                    print("\n===================")
                    print(judul_materi)
                    print("")
                    self.click_materi(judul_materi)
                    self.HalamanKedua.judul_halaman_pertama = judul_materi
                    self.HalamanKedua.proses_materi()
                    print("===================\n")
                    self.Checkpoint.tulis_ke_file_checkpoint(self.fnama_checkpoint, judul_materi)
                    self.ambil_list_materi()

        else:
            pass
