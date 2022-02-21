import time
from hashlib import md5

import qrcode
import requests
from bs4 import BeautifulSoup

from .encrypt import NeteaseMusicEncrypt
from .urls import *
from .config import *
from .record import *
from .singer import *


class NeteaseMusicUser:
    def __init__(self, id: int, config: NeteaseMusicConfigUser = None) -> None:
        self.isLogin: bool = NeteaseMusicConfig.isLogin(id)
        self.config: NeteaseMusicConfigUser = NeteaseMusicConfig.get_config(
            id) if config is None else config
        self.id = id
        r = BeautifulSoup(requests.get(URL_USER_HOME %
                                       id, headers={"cookie": self.config.toCookie()}).text, features="html.parser")
        if r.find("div", class_="n-for404") != None:
            print(f"404 id为{self.id}账户不存在")
            self.allListen = -1
            self.record = NeteaseMusicRecord(self)
            return
        self.allListen = int(
            r.find("div", id="rHeader").h4.string.split("歌")[1][:-1])
        f = r.find("div", class_="name f-cb").find("a", hidefocus="true")
        self.singer = NeteaseMusicSinger(
            int(f["href"].split("=")[1])) if f.has_attr("href") else None
        self.record = NeteaseMusicRecord(self)
        self.getLoginDays()

    def getLoginDays(self):
        dpl=[2,7,15,30,60,120,200,300,450,800]
        spl=[10,40,70,130,200,400,1000,3000,8000,20000]
        r=NeteaseMusicEncrypt.neteaseMusicPost(URL_USER_LEVEL,{"csrf_token":NeteaseMusicConfig.get_default_config().csrf})
        self.level=r["data"]["level"]
        self.loginDays=r["data"]["nowLoginCount"]
        self.playSongs=r["data"]["nowPlayCount"]
        for i in range(self.level):
            self.loginDays+=dpl[i]
            self.playSongs+=spl[i]

    @staticmethod
    def createWithConfig(config: NeteaseMusicConfigUser):
        return NeteaseMusicUser(config.id, config)

    @staticmethod
    def login_text(phone: int, password: str):
        if len(str(phone)) != 11:
            print("手机号必须为11位")
            return
        m = md5(str(password).encode("utf-8")).hexdigest()
        s = requests.Session()
        c = str({"password": m, "phone": str(phone),
                 "checkToken": "9ca17ae2e6ffcda170e2e6eed4d225aabd879ac1408eb48eb2c14f869e9ebaaa73899b9dd0cb59ba97bab5b52af0feaec3b92a888ea586d379b7be9cccd44e868b9bb6d15a9bafa783c854f589acd7f97cfb98ee9e"})
        r = s.post(URL_USER_CELLPHONE, NeteaseMusicEncrypt.join(
            NeteaseMusicEncrypt.neteaseMusicEncrypt(c)), headers=header)
        print(s.cookies)
        q = r.json()
        k = s.cookies
        if q["code"] == 200:
            u = NeteaseMusicConfigUser(q["profile"]["userId"], NeteaseMusicConfig.get_all_config() == [],
                                       q["profile"]["nickname"],  k.get("MUSIC_U"), k.get("__csrf"), k.get("NMTID"))
            NeteaseMusicConfig.login(u)
            print(u.toUser())
        elif q["code"] == 502 or q["code"] == 501:
            print(q["msg"])
        elif q["code"] == 400:
            print("请稍后再试，Responce:", q)
        else:
            print(f"遇到问题{q['code']}，Response:\n", q)

    @staticmethod
    def login():
        c = '{"type":"1","csrf_token":""}'
        r = NeteaseMusicEncrypt.neteaseMusicPost(URL_USER_UNIKEY, c)
        key = r["unikey"]
        print("key:", key)
        print("url:", URL_USER_QRCODE % key)
        print("请用网易云音乐APP扫描二维码授权登录")
        cc = str({"csrf_token": "", "key": key, "type": "1"})
        q = qrcode.QRCode()
        q.add_data(URL_USER_QRCODE % key)
        im = q.make_image()
        im.show()
        t = 0
        while True:
            t += 1
            q = NeteaseMusicEncrypt.neteaseMusicPost(URL_USER_LOGIN, cc)
            time.sleep(0.5)
            print("次数: ", t, q)
            if q["code"] == 802:
                break
            elif q["code"] == 800:
                print("即将重试")
                time.sleep(1)
                NeteaseMusicUser.login()
                return
        w = requests.Session()
        while True:
            t += 1
            q = NeteaseMusicEncrypt.neteaseMusicEncrypt(cc)
            time.sleep(0.5)
            re = w.post(URL_USER_LOGIN, NeteaseMusicEncrypt.join(q),
                        headers={"Content-Type": "application/x-www-form-urlencoded"}).json()
            print("次数: ", t, re)
            if re["code"] == 803:
                break
            elif re["code"] == -460:
                print("登录次数过多")
                break
        csrf = w.cookies.get("__csrf")
        s = w.post(URL_USER_GET % csrf, NeteaseMusicEncrypt.join(
            NeteaseMusicEncrypt.neteaseMusicEncrypt(str({"csrf_token": csrf}))), headers=header).json()
        id = s["profile"]["userId"]
        name = s["profile"]["nickname"]
        co = {"id": id, "nickName": name, "lastSignDate": -1, "MUSIC_U": w.cookies.get(
            "MUSIC_U"), "NMTID": w.cookies.get("NMTID"), "__csrf": csrf}
        co["isDefault"] = NeteaseMusicConfig.get_all_config() == []
        f = NeteaseMusicConfigUser.createWithDict(co)
        print(f"要登录的账号是: {f.nickName}({f.id}) cookie: {f.toCookie()}")
        NeteaseMusicConfig.login(f)
        print("登录成功")
        print("已设置为默认账户" if co["isDefault"] else "")
        return NeteaseMusicUser(id)

    @staticmethod
    def sign_cc():
        NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).sign()

    def sign(self):
        if not self.isLogin:
            raise NeteaseMusicConfigBase.NotLoginError()
        v = self.config

        t = time.strftime("%Y%m%d", time.localtime())
        if t == str(v.lastSignDate):
            print("已经签到了")
            return
        c = str({"type": 1, "csrf_token": self.config.csrf})
        r = NeteaseMusicEncrypt.neteaseMusicPost(
            URL_USER_SIGN % self.config.csrf, c, self.config.toCookie())
        if r["code"] == 200:
            v.updateLastSignDate(t)
            print("签到成功")
        else:
            print(f"签到失败，详情: {r}")
            if r["code"] == -2:
                v.updateLastSignDate(t)
