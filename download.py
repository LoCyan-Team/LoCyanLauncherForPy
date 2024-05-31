"""
TODO: LoCyan Cloud Drive 下载支持
目前能下载的方式：
GitHub Releases：https://github.com/LoCyan-Team/LoCyanFrpPureApp/releases/
YanMo Object: https://objects.ymbit.cn/locyanfrp/
LoCyan Cloud Drive: https://download.locyan.cn/locyanfrp/PureFrpc 傻逼DYC你自己去支持去
YanMo API: https://api.ymbit.cn/public/files/locyanfrp/
"""

from tqdm import tqdm

import io
import platform
import aiohttp
import aiofiles
import zipfile
import os


async def download_frp(url, file_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 LoCyanFrp/1.0.0.24"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                # 获取文件总大小
                total_size = int(response.headers.get("content-length", 0))
                # 初始化tqdm进度条，total为文件总大小
                with tqdm(
                    total=total_size, unit="B", unit_scale=True, desc=file_name
                ) as pbar:
                    # 使用异步写入方式将文件内容写入本地
                    with open(file_name, "wb") as f:
                        downloaded = 0
                        while True:
                            chunk = await response.content.read(1024)  # 每次读取1KB数据
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)  # 累加已下载字节数
                            pbar.update(len(chunk))
                        print(f"文件 {file_name} 下载完成。")


def check_file_exists(file_path):
    return os.path.exists(file_path)


async def check_frp_exists():
    file_path = "./data/frpc.exe"
    if check_file_exists(file_path):
        pass
    else:
        confirm_download = input("你似乎没有下载Frpc，是否需要下载？(y/N)")
        if confirm_download == "y":
            await download_frp()
        else:
            pass


async def unzip_file(file_name):
    async with aiofiles.open(file_name, "rb") as f:
        zip_data = await f.read()
    zip_ref = zipfile.ZipFile(io.BytesIO(zip_data), "r")
    for name in zip_ref.namelist():
        zip_ref.extract(name)
    zip_ref.close()  # 关闭 zip 文件对象


async def main():
    operating_system = platform.system()
    platform_type = platform.machine()

    int(
        input(
            "请列出使用哪一个下载源\n1.GitHub Releases（国内速度慢，但是能保持最新）\n2.YanMo Objects（YanMo个人云存储，方便第三方调用）\n3.LoCyan Cloud "
            "Drive（官方云盘）（尚未支持）\n4. YanMo API(较为稳定，但是更新不会很快)"
        )
    )
    download_version = int(input("请输入你想使用的LoCyanFrp版本号"))
    if download_version == "":
        download_version = "0.51.3"
    else:
        if download_version == int:
            pass
        else:
            print()
    url_list = [
        1,
        f"https://github.com/LoCyan-Team/LoCyanFrpPureApp/releases/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.tar.gz",
        2,
        f"https://objects.ymbit.cn/locyanfrp/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.tar.gz",
        3,
        f"",
        4,
        f"https://api.ymbit.cn/public/locyanfrp/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.tar.gz",
    ]
    file_name = "frp_LoCyanFrp-0.51.3_windows_amd64.zip"
    await download_frp(url_list, file_name)
