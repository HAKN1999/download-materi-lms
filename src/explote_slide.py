from pathlib import Path
import os
import re

from helper.selenium_driver import SeleniumDriver
from utilities.checkpoint import CheckPoint
from utilities.better_text import clean_string
from src.download_materi import DownloadMateri


class SlidePPT(SeleniumDriver):
    def __init__(self, driver):
        self.fname_materi_checkpoint = "slide_checkpoint.txt"
        self.driver = driver
        self.Checkpoint = CheckPoint()
        self.Download_materi = DownloadMateri()
        self.target_url = "https://km-slide.sirogu.com/"
        super().__init__(driver)

    # selector
    _lihat_tautan = "//*[text()='LIHAT TAUTAN']"
    _selanjutnya = "//*[text()='Selanjutnya']"
    _slide_element = "//div[@class='css-12fjjjk']//div[@class='css-1u8plg8']"
    _breadcum = "//div[@class='css-107gr1z']/div[@class='css-1akgoq9']"
    _judul_materi_slide = "//*[@class='css-1sbaybp']"
    _lihat_selanjutnya_xpath = "//*[text()='LIHAT SELENGKAPNYA']"
    _iformat_xpath = "//div[@class='css-zt9xvf']//div[@class='css-1oz15y2']//p[@class='css-34ak08']"

    def check_valid_attribute_class(self, text):
        xpath = f"//*[text()='{text}']"
        self.waitForElementPresent(xpath, "xpath")
        is_presence, elements = self.elementPresence(xpath, "xpath")
        if is_presence:
            attr_class = ""
            if len(elements) > 1:
                attr_class = elements[1].get_attribute("class")
            else:
                attr_class = elements[0].get_attribute("class")
            return attr_class

    def click_side(self, text):
        for _ in range(10):
            ok = self.click_lihat_selanjutnya()
            if ok == False:
                break

        attr_class = self.check_valid_attribute_class(text)
        xpath = f"//*[contains(@class,'{attr_class}') and text()='{text}']"
        elm = self.waitForElement(xpath, "xpath")
        if elm is not None:
            elm.click()

        self.proses_konfirmasi(text)

    def ambil_list_element_slide(self):
        self.waitForElementPresent(self._slide_element, "xpath")
        is_presence, elements = self.elementPresence(self._slide_element, "xpath")
        if is_presence:
            return elements
        return False

    def click_lihat_tautan(self, idx):
        self.fname_materi = self.ambil_judul_materi(idx)
        print(f"Download: {self.fname_materi}")
        elm = self.waitForElement(self._lihat_tautan, "xpath")
        if elm is not None:
            elm.click()

    def click_selanjutnya(self):
        elm = self.waitForElement(self._selanjutnya, "xpath")
        if elm is not None:
            elm.click()

    def ambil_attribute_iframe(self):
        xpath = "//iframe"
        element = self.waitForElementPresent(xpath, "xpath")
        if element is not None:
            link = element.get_attribute("src")
            return link
        return False

    def pindah_new_tab(self):
        # self.waitForElementPresent("p", "id")
        self.driver.implicitly_wait(10)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        url = self.driver.current_url
        if self.target_url in url:
            self.Download_materi.downlod_slide_ppt(self.download_path, url, self.fname_materi)
        else:
            resp = self.ambil_attribute_iframe()
            link = ""
            if isinstance(resp, str):
                link = resp
            self.Download_materi.download_selain_slide_ppt(self.download_path, url, self.fname_materi, link)

    def pindah_tab_utama(self):
        self.waitForElementPresent(self._breadcum, "xpath")
        self.driver.switch_to.window(self.driver.window_handles[0])

    def ambil_judul_materi_disidebar(self):
        xpath = "//p[@class='css-1jtvebl']"
        self.waitForElementPresent(xpath, "xpath")
        is_presence, elements = self.elementPresence(xpath, "xpath")
        list_judul_materi = []
        if is_presence:
            for element in elements:
                t = element.text
                list_judul_materi.append(t)
            return list_judul_materi
        else:
            return False

    def ambil_judul_materi(self, idx):
        element = self.waitForElementPresent(self._judul_materi_slide, "xpath")

        if element is not None:
            slide_name = clean_string(element.text)
            return f"{idx}_{slide_name}"
        else:
            resp = self.ambil_judul_materi_disidebar()
            if isinstance(resp, list):
                return resp
        return f"{idx}_"

    def check_apakah_materi_video(self):
        xpath = "//div[@class='css-wtaal9-MissionVideoView']"
        self.waitForElementPresent(xpath)
        is_presence, ok = self.isElementPresent(xpath, "xpath")
        if is_presence:
            return True
        else:
            return False

    def proses_explore_slide(self, list_element):
        for idx, _ in enumerate(list_element, start=1):
            ok = self.check_apakah_materi_video()
            if ok == False:
                self.click_lihat_tautan(idx)
                self.pindah_new_tab()

                # print(len(self.driver.window_handles))
                if len(self.driver.window_handles) != 1:
                    self.driver.close()

                self.pindah_tab_utama()
                self.click_selanjutnya()
            else:
                return

        self.driver.back()
        self.pindah_tab_utama()

    def click_lihat_selanjutnya(self):
        element = self.waitForElement(self._lihat_selanjutnya_xpath, "xpath")
        if element is not None:
            element.click()
            return True
        else:
            return False

    def click_tutup(self):
        elm = self.waitForElementPresent(self._iformat_xpath, "xpath")
        text = ""
        if elm is not None:
            text = elm.text.lower()

        if text != "" and "tutup" in text:
            elm = self.waitForElement(self._iformat_xpath, "xpath")
            if elm is not None:
                elm.click()
                return True
        return False

    def click_hadir(self):
        elm = self.waitForElement(self._iformat_xpath, "xpath")
        if elm is not None:
            elm.click()
            return True
        return False

    def proses_konfirmasi(self, v):
        resp = self.click_tutup()
        if resp:
            self.Checkpoint.tulis_ke_file_checkpoint(self.fname_materi_checkpoint, v)
        else:
            resp = self.click_hadir()
            if resp:
                self.click_side(v)

    def buat_folder(self, path):
        if os.path.isdir(path) != True:
            os.makedirs(path, exist_ok=True)

    def proses_slide(self, resp, judul_halaman_utama, multi_materi=False):
        folder_utama = clean_string(judul_halaman_utama)
        for idxx, i in enumerate(resp, start=1):
            for k, v in i.items():
                folder_kedua = clean_string(k)
                for idx, v in enumerate(v, start=1):
                    folder_materi = clean_string(v)
                    print(f"* proses: {v}")
                    self.download_path = (
                        Path.cwd()
                        / "RUANG-GURU-MATERI"
                        / folder_utama
                        / f"{idxx}_{folder_kedua}"
                        / f"{idx}_{folder_materi}"
                    )

                    # print(self.download_path)
                    status, msg = self.Checkpoint.baca_file_checkpoint(self.fname_materi_checkpoint, v)

                    if status != True:
                        self.buat_folder(self.download_path)
                        self.click_side(v)
                        all_slide = self.ambil_list_element_slide()
                        if all_slide is not False:
                            # self.total_slide = len(all_slide)
                            self.proses_explore_slide(all_slide)
                            self.Checkpoint.tulis_ke_file_checkpoint(self.fname_materi_checkpoint, v)
                            self.Download_materi.downoad_slide_ppt_2()
                        else:
                            print("tidak ada slide")
                            self.Checkpoint.tulis_ke_file_checkpoint(self.fname_materi_checkpoint, v)
                            self.driver.back()

                        self.driver.back()
