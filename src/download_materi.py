import os
import subprocess


class DownloadMateri:
    def __init__(self) -> None:
        self._tmp_url = []
        self._tmp_path = []
        self._fname = []

    def download_selain_slide_ppt(self, path, url, materi, link):
        self.buat_folder(path)
        fname = os.path.split(path)[-1]
        new_path = os.path.join(path, f"referensi_{fname}.txt")
        with open(new_path, "a") as f:
            f.write(f"Materi: {materi}\n")
            f.write(f"Sumber: {link}\n")
            f.write(f"url   : {url}\n\n")

    def downlod_slide_ppt(self, path, url, fname):
        self._tmp_url.append(url)
        self._tmp_path.append(path)
        self._fname.append(fname)

        self.buat_folder(path)
        cmd = f"wget -P '{path}' -E -H -k -p {url} -o download.log"
        subprocess.run(cmd, shell=True)

    def downoad_slide_ppt_2(self):
        if len(self._tmp_path) != 0:
            print("* Download format PDF")
            for url, path, pdf_name in zip(self._tmp_url, self._tmp_path, self._fname):
                print(url)
                new_path = os.path.join(path, "PDF_FILE")
                self.buat_folder(new_path)
                cmd = f"google-chrome --headless --disable-gpu --print-to-pdf={new_path}/{pdf_name}.pdf {url} "
                subprocess.run(cmd, shell=True)

        self._tmp_path.clear()
        self._tmp_url.clear()
        self._fname.clear()

    def buat_folder(self, path):
        if os.path.isdir(path) != True:
            os.makedirs(path, exist_ok=True)
