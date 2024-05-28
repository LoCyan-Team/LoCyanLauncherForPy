"""
TODO:目前因为服务器技术升级，目前这种下载方式是不可行的。只能过几天再改改，且 YanMo API 的海外下载会触发 Cloudflare WAF 的咨询，UA值还得简单修改
目前能下载的方式：
GitHub Releases：https://github.com/LoCyan-Team/LoCyanFrpPureApp/releases/
YanMo API: https://api.ymbit.cn/public/files/locyanfrp/
LoCyan Cloud Drive: https://download.locyan.cn/locyanfrp/PureFrpc
"""

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
            requests.get("https://api.ymbit.cn/public/files/locyanfrp/", stream=True)
        elif os_name.lower() == "darwin":
            requests.get("https://mirrors.nyanest.xyz/locyan/frpc", stream=True)
        else:
            print("暂不支持此架构")
