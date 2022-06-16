import os
from typing import Tuple, Union


class CheckPoint:
    def is_exists_file_checkpoint(self, file: str) -> bool:
        if os.path.exists(file):
            return True
        else:
            with open(file, "w") as f:
                f.write("")
        return False

    def baca_file_checkpoint(self, file: str, tgt_materi: str) -> Tuple[bool, str]:
        file_ditemukan = self.is_exists_file_checkpoint(file)
        if file_ditemukan:
            with open(file, "r") as f:
                datas = f.readlines()

            for data in datas:
                if len(data) != 0:
                    split_data = data.split(",")

                    # if len(split_data) != 0:
                    nama_materi = split_data[:-1][0]
                    status = split_data[-1]

                    if nama_materi in tgt_materi and "ok" in status:
                        return True, "ok"

                    elif nama_materi in tgt_materi and "error" in status:
                        return True, "error"

        return False, ""

    def tulis_ke_file_checkpoint(
        self, file: str, tgt_materi: str, status: str = None
    ) -> None:
        ok, _ = self.baca_file_checkpoint(file, tgt_materi)
        if ok:
            return

        else:
            with open(file, "a") as f:
                materi = f"{tgt_materi}, ok\n"

                if status != None:
                    materi = f"{tgt_materi}, {status}\n"

                f.write(materi)
