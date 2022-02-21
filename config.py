
from .AquaCore.config import BaseConfig, BaseConfigUser
from .urls import *
from .encrypt import NeteaseMusicEncrypt
from typing import Any, Dict, List, Union
NeteaseMusicBuffer: Dict[str, Any] = {}





class NeteaseMusicConfigUser(BaseConfigUser):
    def __init__(self, id: int, isDefault: bool, nickName, MusicU, csrf, nmtid, lastSignDate=-1) -> None:
        self.lastSignDate: int = lastSignDate
        self.nickName: str = nickName
        self.id: int = id
        self.MusicU: str = MusicU
        self.csrf: str = csrf
        self.nmtid: str = nmtid
        super().__init__(id, isDefault,
                         **{"nickName": nickName, "MUSIC_U": MusicU, "__csrf": csrf, "NMTID": nmtid, "lastSignDate": lastSignDate})

    def updateLastSignDate(self, date: int):
        NeteaseMusicConfig.updateLastSignDate(self, date)

    @classmethod
    def createWithDict(cls, dt: Dict[str, Any]):
        return cls(dt["id"], dt["isDefault"], dt["nickName"], dt["MUSIC_U"], dt["__csrf"], dt["NMTID"], dt["lastSignDate"])

    def toUser(self) -> str:
        return f"{self.nickName}({self.id}) cookie:{self.toCookie()}"

    def toCookie(self) -> str:
        return f"MUSIC_U={self.MusicU}; NMTID={self.nmtid}; __csrf={self.csrf}"

    def isLogin(self) -> bool:
        return NeteaseMusicConfig.isLogin(self.id)


class NeteaseMusicConfigBase(BaseConfig):
    def __init__(self) -> None:
        self.file_path = r"D:\Program Source\AwesomeCore_git\NeteaseMusic.json"
        self.type = NeteaseMusicConfigUser

    @staticmethod
    def returnThis():
        return NeteaseMusicConfig

    def updateLastSignDate(self, data: NeteaseMusicConfigUser, date: int):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            d = eval(f.read())
            i = [j["id"] for j in d]
            if data.id not in i:
                raise self.NotLoginError()
            v = d[i.index(data.id)]
            v["lastSignDate"] = date
            self.lastSignDate = date
            f.seek(0)
            f.truncate()
            f.write(str(d).replace("'", '"'))

    def login(self, data: NeteaseMusicConfigUser):
        super().login(data)

    def login_cc(self, id: int, csrf: str, musicU: str):
        r = NeteaseMusicEncrypt.neteaseMusicPost(URL_USER_GET % csrf, str(
            {"csrf_token":csrf}), cookies=f"MUSIC_U={musicU}; __csrf={csrf}")
        if r["account"] is None and r["profile"] is None:
            raise ValueError("账户错误")
        name = r["profile"]["nickname"]
        u = NeteaseMusicConfigUser(id, self.get_all_config() == [],
                                   name, musicU, csrf, '')
        self.login(u)
        print(f"{name}({id})登录成功", u.toUser())

    def get_default_config(self) -> NeteaseMusicConfigUser:
        if "DEFAULT_CONFIG_PAGE" not in NeteaseMusicBuffer:
            c = super().get_default_config()
            NeteaseMusicBuffer["DEFAULT_CONFIG_PAGE"] = c
            return c
        else:
            return NeteaseMusicBuffer["DEFAULT_CONFIG_PAGE"]

    def get_default_config_cc(self):
        c: NeteaseMusicConfigUser = super().get_default_config()
        print(c.toUser())

    def get_all_config(self) -> List[NeteaseMusicConfigUser]:
        return super().get_all_config()

    def get_config(self, id: int) -> NeteaseMusicConfigUser:
        return super().get_config(id)


NeteaseMusicConfig: NeteaseMusicConfigBase = NeteaseMusicConfigBase()
