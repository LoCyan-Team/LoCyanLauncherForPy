import os
import sys
import platform


def get_launch_conf_no_http(ip, port, user, type1, lip, lp, rp, proxyname):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

    old_no_http = """[common]
server_addr = [serverip]
server_port = [serverport]
tcp_mux = true
protocol = tcp
user = [user]
token = LoCyanToken
dns_server = 114.114.114.114

[[proxyname]]
privilege_mode = true
type = [type]
local_ip = [lip]
local_port = [lp]
remote_port = [rp]
use_encryption = true
use_compression = true
    """

    new_nohttp = old_no_http.replace("[serverip]", ip)
    new_nohttp = new_nohttp.replace("[serverport]", port)
    new_nohttp = new_nohttp.replace("[user]", user)
    new_nohttp = new_nohttp.replace("[lip]", lip)
    new_nohttp = new_nohttp.replace("[lp]", lp)
    new_nohttp = new_nohttp.replace("[type]", type1)
    new_nohttp = new_nohttp.replace("[rp]", rp)
    new_nohttp = new_nohttp.replace("[proxyname]", proxyname)
    print(new_nohttp)
    with open(dirname + "\\frpc.ini", mode="w") as f:
        f.write(new_nohttp)
        f.close()


def get_launch_conf_http(ip, port, user, type1, lip, lp, rp, proxyname, cd):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    old_http = """[common]
server_addr = [serverip]
server_port = [serverport]
tcp_mux = true
protocol = tcp
user = [user]
token = LoCyanToken
dns_server = 114.114.114.114

[[proxyname]]
privilege_mode = true
type = [type]
local_ip = [lip]
local_port = [lp]
remote_port = [rp]
custom_domains = [cd]
use_encryption = true
use_compression = true
    """

    new_http = old_http.replace("[serverip]", ip)
    new_http = new_http.replace("[serverport]", port)
    new_http = new_http.replace("[user]", user)
    new_http = new_http.replace("[lip]", lip)
    new_http = new_http.replace("[lp]", lp)
    new_http = new_http.replace("[type]", type1)
    new_http = new_http.replace("[rp]", rp)
    new_http = new_http.replace("[proxyname]", proxyname)
    new_http = new_http.replace("[cd]", cd)
    new_http = new_http.replace('["', "")
    new_http = new_http.replace('"]', "")
    print(new_http)
    with open(dirname + "\\frpc.ini", mode="w") as f:
        f.write(new_http)
        f.close()


def more_proxy_nohttp(ip, port, lip, lp, type1, rp, proxyname):
    more_nohttp = """
[[proxyname]]
privilege_mode = true
type = [type]
local_ip = [lip]
local_port = [lp]
remote_port = [rp]
use_encryption = true
use_compression = true
    """
    new_more_nohttp = more_nohttp.replace("[serverip]", ip)
    new_more_nohttp = new_more_nohttp.replace("[serverport]", port)
    new_more_nohttp = new_more_nohttp.replace("[lip]", lip)
    new_more_nohttp = new_more_nohttp.replace("[lp]", lp)
    new_more_nohttp = new_more_nohttp.replace("[type]", type1)
    new_more_nohttp = new_more_nohttp.replace("[rp]", rp)
    new_more_nohttp = new_more_nohttp.replace("[proxyname]", proxyname)
    f = open("frpc.ini", "r", encoding="utf-8")
    before_contents = f.read()
    f.close()
    f = open("frpc.ini", "w", encoding="utf-8")
    f.write(before_contents + new_more_nohttp)
    f.close()


def more_proxy_http(ip, port, lip, lp, type1, rp, proxyname, cd):
    more_http = """

[[proxyname]]
privilege_mode = true
type = [type]
local_ip = [lip]
local_port = [lp]
remote_port = [rp]
custom_domains = [cd]
use_encryption = true
use_compression = true
    """
    new_more_http = more_http.replace("[serverip]", ip)
    new_more_http = new_more_http.replace("[serverport]", port)
    new_more_http = new_more_http.replace("[lip]", lip)
    new_more_http = new_more_http.replace("[lp]", lp)
    new_more_http = new_more_http.replace("[type]", type1)
    new_more_http = new_more_http.replace("[rp]", rp)
    new_more_http = new_more_http.replace("[proxyname]", proxyname)
    new_more_http = new_more_http.replace("[cd]", cd)
    new_more_http = new_more_http.replace('["', "")
    new_more_http = new_more_http.replace('"]', "")
    f = open("frpc.ini", "r", encoding="utf-8")
    before_contents = f.read()
    f.close()
    f = open("frpc.ini", "w", encoding="utf-8")
    f.write(before_contents + new_more_http)
    f.close()


def add_proxy_header(ip, port, user):
    header = """
[common]
server_addr = [serverip]
server_port = [serverport]
tcp_mux = true
protocol = tcp
user = [user]
token = LoCyanToken
dns_server = 114.114.114.114
"""
    new_header = header.replace("[serverip]", ip)
    new_header = new_header.replace("[serverport]", port)
    new_header = new_header.replace("[user]", user)
    f = open("frpc.ini", "w", encoding="utf-8")
    f.write(new_header)
    f.close()


def launchfrp():
    if platform.system().lower() == "windows":
        os.system("frpc.exe -c frpc.ini")
    else:
        os.system("./frpc -c frpc.ini")
