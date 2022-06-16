from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from src.halaman_login import HalamanLogin
from src.halaman_utama import HalamanUtama
from src.halaman_kedua import HalamanKedua

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    email = "aa@gmail.com"
    password = ""

    appLogin = HalamanLogin(driver)
    appLogin.login(email, password)
    appLogin.verify_login_successful()

    appHalamanUtama = HalamanUtama(driver)
    appHalamanUtama.ambil_list_materi()

    appHalamanKedua = HalamanKedua(driver)
    appHalamanKedua.proses_materi()
