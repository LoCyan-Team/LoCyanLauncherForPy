"""
TODO: LoCyan Cloud Drive 下载支持
目前能下载的方式：
GitHub Releases：https://github.com/LoCyan-Team/LoCyanFrpPureApp/releases/
YanMo Object: https://objects.ymbit.cn/locyanfrp/
LoCyan Cloud Drive: https://alist.locyan.cn/d/locyanfrp/PureFrpc/
YanMo API: https://api.ymbit.cn/public/files/locyanfrp/
"""

from tqdm import tqdm

import asyncio
import io
import platform
import aiohttp
import aiofiles
import zipfile
import os
import sys


async def download_frp(url, file_name):
    def detect_desktop_environment():
        if platform.system() == "Windows":
            platform.system() + " " + platform.release()
        elif platform.system() == "Linux":
            os.environ.get("XDG_CURRENT_DESKTOP")
        else:
            confirm_continue = input(
                "无法获取系统桌面环境，可能会导致未知错误，是否继续？(y/N)"
            )
            if confirm_continue == "y":
                os.environ.get("Unknown")
            elif confirm_continue == "N":
                sys.exit(1)
            else:
                return detect_desktop_environment()

    system = platform.system()
    headers = {
        "User-Agent": f"Mozilla/5.0 ({detect_desktop_environment}; {system}; x64; rv:127.0) Gecko/20100101 "
        f"LoCyanFrp/1.0.0.24"
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


async def check_file_exists(file_path):
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
    download_version = int(
        input("请输入你想使用的LoCyanFrp版本号（直接回车则默认使用最新版本）")
    )
    if download_version == "":
        download_version = "0.51.3"
    else:
        if download_version == int:
            pass
        else:
            print()
    if platform.system() == "Windows":
        url_list = [
            1,
            f"https://github.com/LoCyan-Team/LoCyanFrpPureApp/releases/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.zip",
            2,
            f"https://objects.ymbit.cn/locyanfrp/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.zip",
            3,
            f"",
            4,
            f"https://api.ymbit.cn/public/locyanfrp/frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.zip",
        ]
    else:
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
    if platform.system() == "Windows":
        file_name = (
            f"frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.zip"
        )
    else:
        file_name = f"frp_LoCyanFrp-{download_version}_{operating_system}_{platform_type}.tar.gz"
    await download_frp(url_list, file_name)
    await unzip_file(file_name)
    await check_frp_exists()


if __name__ == "__main__":
    asyncio.run(main())
