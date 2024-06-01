import urllib3
import requests
import download
import asyncio

from launch import *


# 定义主类
class Main:
    url = "https://www.locyanfrp.cn/api/"
    proxy_temp = ""  # 用户所持有隧道ID暂存
    proxy_list_id_type = {}
    r = None

    def __init__(self):
        # 关闭keep-alive
        self.r = requests.session()
        self.r.keep_alive = False
        # 设置重连次数为5
        self.r.DEFAULT_RETRIES = 5
        # 关闭urllib3不验证SSL产生的报错
        urllib3.disable_warnings()

        async def async_init(self):
            # 检查更新
            version = "version_1.0.1"

            check_update_url = (
                f"https://api.ymbit.cn/public/check_update/{version}.html"
            )
            check_update = requests.get(check_update_url, verify=False)

            if check_update.status_code == 200:
                await download.check_frp_exists()
            elif check_update.status_code == 404:
                print("目前 LoCyanPyLauncher 非最新版本，请前往 GitHub 更新。")
            else:
                print("检查更新失败，请检查网络连接。")
                sys.exit(1)

            print("欢迎使用LoCyan Frp Application")
            result = self.r.get("https://api.locyanfrp.cn/App", verify=False)
            result = result.json()
            contents = result["contents"]
            print("------------------------------------------------")
            print("公告：")
            print(contents)
            print("------------------------------------------------")

    def get_user_info(
        self, node: str, code: str
    ):  # 使用FrpPanel自带的API进行鉴权，判断用户是否有权限使用
        result = self.r.get(
            self.url
            + "?apitoken=LoCyanToken|"
            + node
            + "&user="
            + code
            + "&action=checktoken",
            verify=False,
        )
        return result.text

    def get_server_list(self):  # 获取所有服务器列表
        url = "https://api.locyanfrp.cn/api/v2/proxies/getlist"
        rs = self.r.get(url, verify=False).json()
        for i in rs:
            server_id = i["id"]
            server_name = i["name"]
            server_ip = i["hostname"]
            status = i["status"]
            if status == "200":
                print("ID:", server_id, "|", server_name, "[", server_ip, "]")

    def get_name_by_code(self, code):  # 通过token获取用户名
        url = "https://api.locyanfrp.cn/Account/GetUserNameByFrpToken?token=" + code
        rs = self.r.get(url, verify=False).json()
        username = rs["username"]
        return username

    def getproxy(self, node, user):  # 通过用户名获取用户隧道
        url = (
            "https://api.locyanfrp.cn/Proxies/GetProxiesListByNode?node="
            + node
            + "&username="
            + user
        )
        rs = self.r.get(url, verify=False).json()

        # 检查是否有隧道存在
        if rs["count"] == 0:
            return None
        else:
            # rs["proxies"] 是个列表
            for i in rs["proxies"]:
                # 鬼知道为什么本地端口是整数，然后远程是字符串
                print(
                    "ID:",
                    i["id"],
                    "|",
                    i["proxy_name"],
                    "[",
                    i["proxy_type"],
                    "]",
                    str(i["local_port"]),
                    "->",
                    i["remote_port"],
                )
                if len(self.proxy_temp) == 0:
                    self.proxy_list_id_type[str(i["id"])] = i["proxy_type"]
                    self.proxy_temp = str(i["id"])
                else:
                    self.proxy_list_id_type[str(i["id"])] = i["proxy_type"]
                    self.proxy_temp = self.proxy_temp + " | " + str(i["id"])

    def is_proxy_in_user(self):  # 检查该隧道是否为该用户所有
        if self.proxy_temp.find(proxyid) >= 0:
            return 0
        else:
            return -1

    def get_server_info(self, id):
        url = "https://api.locyanfrp.cn/Proxies/GetServerInfoByNode?node=" + id
        rs = self.r.get(url, verify=False).json()
        server_id = rs["id"]
        server_name = rs["name"]
        server_ip = rs["hostname"]
        server_port = rs["port"]
        status = rs["status"]
        return str(server_ip) + "|" + str(server_port)

    def get_proxy_info(self, user, id1):
        url = (
            "https://api.locyanfrp.cn/Proxies/GetProxiesListByID?username="
            + user
            + "&id="
            + id1
        )
        rs = self.r.get(url, verify=False).json()
        # type1, lip, lp, rp, proxyname, cd
        # rs["proxies"]是列表
        for type in rs["proxies"]:
            # type[3]:type[4]:lip type[5]:lp type[11] rp type[8]:自定义域名(cd)
            if (
                self.proxy_list_id_type[id1] == "http"
                or self.proxy_list_id_type[id1] == "https"
            ):
                return (
                    str(type["proxy_type"])
                    + "|"
                    + str(type["local_ip"])
                    + "|"
                    + str(type["local_port"])
                    + "|"
                    + str(type["remote_port"])
                    + "|"
                    + str(type["proxy_name"])
                    + "|"
                    + type["domain"]
                )
            else:
                return (
                    str(type["proxy_type"])
                    + "|"
                    + str(type["local_ip"])
                    + "|"
                    + str(type["local_port"])
                    + "|"
                    + str(type["remote_port"])
                    + "|"
                    + str(type["proxy_name"])
                )


main = Main()

main.get_server_list()
token_user = ""
if os.path.exists("cfg.ini"):
    f = open("cfg.ini", "r", encoding="utf-8")
    token_user = f.read()
    print(
        "已读取到您上次使用的token: ",
        token_user,
        "如果想要更换的话请在选择服务器的时候输入ct",
    )
    f.close()

while True:
    choose = input("请选择需要映射的服务器：")
    if choose == "ct":
        ct = input("请输入您要更换的token: ")
        f = open("cfg.ini", "w", encoding="utf-8")
        f.write(ct)
        f.close()
        print("更换成功！")
        choose = input("请选择需要映射的服务器：")
        token_user = ct

    if token_user == "":
        token_user = input("请输入您的连接Token: ")
        f = open("cfg.ini", "w", encoding="utf-8")
        f.write(token_user)
        f.close()

    print("开始进行鉴权，请稍等...")
    a = main.get_user_info(choose, token_user)
    if "success" in a:
        token_user_name = main.get_name_by_code(token_user)
        print("鉴权成功，欢迎您，指挥官：" + token_user_name)
        print("支持多开, 请用空格分隔每一个隧道ID, 目前仅支持同一节点的多开")
        while True:  # 反复弹出，直到输入正确
            main.getproxy(node=choose, user=token_user_name)
            proxyid = input(">> ")
            print("选择ID: " + proxyid)
            print("准备启动...")
            ip, port = main.get_server_info(choose).split("|")
            if " " in proxyid:
                print("=========================================")
                print("你可以用这个地址连接你的隧道！")
                print("检测到多个隧道多开，以下为链接方式列表：")
                proxyid = proxyid.split(" ")
                # 会清除frpc.ini内的全部内容，需要第一个执行
                add_proxy_header(ip=ip, port=port, user=token_user)
                for i in proxyid:
                    # 判断是否是HTTPS/HTTP映射，以便判断是否需要获取domain域名
                    try:
                        if (
                            main.proxy_list_id_type[i] == "http"
                            or main.proxy_list_id_type[i] == "https"
                        ):
                            type1, lip, lp, rp, proxyname, cd = main.get_proxy_info(
                                token_user_name, i
                            ).split("|")
                        else:
                            type1, lip, lp, rp, proxyname = main.get_proxy_info(
                                token_user_name, i
                            ).split("|")
                    except KeyError as e:
                        print("隧道不存在!")
                        continue

                    if type1 == "http" or type1 == "https":
                        print("ID: " + i + "连接地址：" + cd)
                        more_proxy_http(
                            ip=ip,
                            port=port,
                            type1=type1,
                            lip=lip,
                            lp=lp,
                            rp=rp,
                            proxyname=proxyname,
                            cd=cd,
                        )
                    else:
                        print("ID: " + i + "连接地址：" + ip + ":" + rp)
                        more_proxy_nohttp(
                            ip=ip,
                            port=port,
                            type1=type1,
                            lip=lip,
                            lp=lp,
                            rp=rp,
                            proxyname=proxyname,
                        )

                print("=========================================")
                launch_frp()
            else:
                print("=========================================")
                print("你可以用这个地址连接你的隧道！")
                # 判断是否是HTTPS/HTTP映射，以便判断是否需要获取domain域名
                try:
                    if (
                        main.proxy_list_id_type[proxyid] == "http"
                        or main.proxy_list_id_type[proxyid] == "https"
                    ):
                        type1, lip, lp, rp, proxyname, cd = main.get_proxy_info(
                            token_user_name, proxyid
                        ).split("|")
                    else:
                        type1, lip, lp, rp, proxyname = main.get_proxy_info(
                            token_user_name, proxyid
                        ).split("|")
                except KeyError as e:
                    print("隧道不存在!")
                    continue
                if type1 == "http" or type1 == "https":
                    print("ID: " + proxyid + "连接地址：" + cd)
                    print("=========================================")
                    get_launch_conf_http(
                        ip=ip,
                        port=port,
                        user=token_user,
                        type1=type1,
                        lip=lip,
                        lp=lp,
                        rp=rp,
                        proxyname=proxyname,
                        cd=cd,
                    )
                else:
                    print("ID: " + proxyid + "连接地址：" + ip + ":" + rp)
                    print("=========================================")
                    get_launch_conf_no_http(
                        ip=ip,
                        port=port,
                        user=token_user,
                        type1=type1,
                        lip=lip,
                        lp=lp,
                        rp=rp,
                        proxyname=proxyname,
                    )

                launch_frp()
            break
        break
    else:
        print(
            "鉴权失败, 请检查您的信息以及你是否有权限使用该服务器, 您可以尝试输入ct更换token秘钥"
        )
        continue
