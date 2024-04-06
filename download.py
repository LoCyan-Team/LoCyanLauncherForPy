import platform
import requests
import os

from tqdm import tqdm


# 封装查询系统架构的函数
def download_frpc():
    if os.path.exists("frpc"):
        os_name = platform.system()
        if os_name.lower() == "windows":
            windows_downloader = requests.get(
                "https://mirrors.nyanest.xyz/locyan/frpc.exe", stream=True
            )
            total = int(windows_downloader.headers.get("content-length", 0))
            with open("frpc.exe", "wb") as file, tqdm(
                desc="frpc.exe",
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in windows_downloader.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
        elif os_name.lower() == "linux":
            requests.get("https://mirrors.nyanest.xyz/locyan/frpc", stream=True)
        elif os_name.lower() == "darwin":
            requests.get("https://mirrors.nyanest.xyz/locyan/frpc", stream=True)
        else:
            print("暂不支持此架构")
