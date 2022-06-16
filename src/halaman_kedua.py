from lxml import html

from helper.selenium_driver import SeleniumDriver
from src.explote_slide import SlidePPT


class HalamanKedua(SeleniumDriver):
    def __init__(self, driver):
        self.driver = driver
        self.Slide_ppt = SlidePPT(driver)
        self.judul_halaman_pertama = None
        super().__init__(driver)

    # selector
    # materi single
    _section_single_materi_xpath = "//div[@class='css-1a0r6m']//div[@class='css-19avji5']"
    _judul_materi_single_xpath = "//p[@class='css-10v7ti5']"
    _sub_judul_materi_single_xpath = "//p[@class='css-coz9iv']"

    # materi multi
    _section_multi_materi_xpath = "//div[@class='css-5ngm4s']//div[@class='css-1l25ls']"
    _judul_materi_multi_xpath = "//p[@class='css-1lqc70j']"
    _sub_judul_multi_materi_xpath = "//p[@class='css-1du2eax']"
    _lihat_selanjutnya_xpath = "//*[text()='LIHAT SELENGKAPNYA']"

    def ambil_judul_materi_single(self, element):
        sc_lxml = html.fromstring(element.get_attribute("innerHTML"))
        elm = sc_lxml.xpath(self._judul_materi_single_xpath)
        if len(elm) != 0:
            return elm[0].text
        return False

    def ambil_sub_judul_material_single(self, element):
        sc_lxml = html.fromstring(element.get_attribute("innerHTML"))
        elm = sc_lxml.xpath(self._sub_judul_materi_single_xpath)
        if len(elm) != 0:
            return elm[0].text
        return False

    def ambil_data_materi_single(self):
        is_presence, list_element = self.elementPresence(self._section_single_materi_xpath, "xpath")
        list_data = []
        if is_presence:
            for element in list_element:
                judul = self.ambil_judul_materi_single(element)
                sub_judul = self.ambil_sub_judul_material_single(element)
                list_data.append(sub_judul)
            return [{judul: list_data}]
        else:
            return False

    def check_materi_single(self):
        element = self.waitForElementPresentVisibility(self._section_single_materi_xpath, "xpath")
        if element is not None:
            return True
        return False

    ########
    #
    #######
    def click_lihat_selanjutnya(self):
        element = self.waitForElement(self._lihat_selanjutnya_xpath, "xpath")
        if element is not None:
            element.click()
            return True
        else:
            return False

    def ambil_judul_materi_multi(self, element):
        sc_lxml = html.fromstring(element.get_attribute("innerHTML"))
        elm = sc_lxml.xpath(self._judul_materi_multi_xpath)
        if len(elm) != 0:
            return elm[0].text
        return False

    def ambil_sub_judul_material_multi(self, element):
        sc_lxml = html.fromstring(element.get_attribute("innerHTML"))
        elm = sc_lxml.xpath(self._sub_judul_multi_materi_xpath)
        if len(elm) != 0:
            return [e.text for e in elm]
        return False

    def ambil_data_materi_multi(self):
        for _ in range(10):
            ok = self.click_lihat_selanjutnya()
            if ok != True:
                break

        is_presence, list_element = self.elementPresence(self._section_multi_materi_xpath, "xpath")
        list_data = []
        if is_presence:
            for element in list_element:
                judul = self.ambil_judul_materi_multi(element)

                # mengambil semua sub judul
                sub_judul = self.ambil_sub_judul_material_multi(element)

                list_data.append({judul: sub_judul})
            return list_data
        else:
            return False

    def check_materi_multi(self):
        element = self.waitForElementPresentVisibility(self._section_multi_materi_xpath, "xpath")
        if element is not None:
            return True
        return False

    def proses_materi(self):
        if self.check_materi_single():
            resp = self.ambil_data_materi_single()
            if isinstance(resp, list):
                # print(resp)
                self.Slide_ppt.proses_slide(resp, self.judul_halaman_pertama)
            else:
                print("Materi single tidak ditemukan")

        elif self.check_materi_multi():
            resp = self.ambil_data_materi_multi()
            if isinstance(resp, list):
                self.Slide_ppt.proses_slide(resp, self.judul_halaman_pertama)
                # print(resp)
            else:
                print("Materi multi tidak ditemukan")
        else:
            print("Tidak ada materi")
