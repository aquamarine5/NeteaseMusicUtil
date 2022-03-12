
from typing import List

from .encrypt import NeteaseMusicEncrypt
from .urls import *
from .user import NeteaseMusicUser
from .config import NeteaseMusicConfig
from .webloader import NeteaseMusicWebLoader


class NeteaseMusicRecord:
    def __init__(self, id: NeteaseMusicWebLoader) -> None:
        self.id = id
        self.data = self.get_user_record(id.id)
        self.allListen = id.allListen
        self.hasPermission = self.data["code"] == 200
        self.allData = self.data["allData"] if self.hasPermission else None
        self.weekData = self.data["weekData"] if self.hasPermission else None

    def get_user_record(self, id: int, isPost: bool = True):
        c = str({"limit": "1000", "offset": "0", "total": "true",
                 "type": "-1", "uid": str(id), "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicEncrypt.neteaseMusicPost(URL_USER_RECORD, c, self.id.config.toCookie()) if isPost else NeteaseMusicEncrypt.neteaseMusicEncrypt(c)
    #######################################

    @staticmethod
    def alltime_cc(i: str):
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        if i == "all":
            self.alltime_all()
        elif i == "week":
            self.alltime_week()

    def alltime_week(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("一周共 168 个小时")
        print(f"这周{round(self.alltime(self.weekData,False)/604800,4)*100}%的时间都在听音乐")

    def alltime_all(self, isSlimp: bool = True):
        if not self.hasPermission:
            raise ValueError("没有权限")
        self.alltime(self.allData, isSlimp)

    def alltime(self, data: List[dict], isSlimp: bool = True):
        def slimp(now: int, target: int, average: int) -> int:
            t = target-100
            tt = t*0.7
            t1 = t*0.3
            tf = t-tt
            offset = tf/now
            a = 0
            for _ in range(now):
                a += average*now*offset
                now -= 1
            a += average*1*t1
            return int(a)

        def second_format(s: int) -> str:
            m = s//60
            ss = s % 60
            hh = m//60
            mm = m % 60

            def fill_to_2(i: int) -> str:
                s = str(i)
                return s if len(s) == 2 else "0"*(2-len(s))+s
            return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"
        alt = 0
        t = 0
        for i in data:
            t += i["song"]["dt"]//1000
            alt += i["song"]["dt"]//1000*i["playCount"]
        if isSlimp and len(data) == 100:
            s = slimp(data[-1]["playCount"], self.allListen, t//len(data))
            a = s+alt
            print("一共听了: ", second_format(alt), "+",
                  second_format(s), "=", second_format(a), "小时的音乐")
        else:
            print("一共听了: ", second_format(alt), "小时的音乐")
            print(f"本周平均每天听 {second_format(alt//7)} 小时的音乐")
        return alt
    #######################################

    @staticmethod
    def analyse_complex():
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        self.analyse_week()
        self.analyse_all()
        self.alltime_week()
        print("AwesomeCore.NeteaseMusic 提供听歌时长分析服务")
        self.alltime_all()
        print(f"一共听了 {self.allListen} 首歌")

    @staticmethod
    def analyse_cc(i: str):
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        if i == "all":
            self.analyse_all()
        elif i == "week":
            self.analyse_week()

    def analyse_week(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("\n====================WEEK DATA ANALYSE:")
        self.analyse(self.weekData)

    def analyse_all(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("\n====================ALL DATA ANALYSE:")
        self.analyse(self.allData)

    def analyse(self, data: List[dict]):
        def second_format(s: int) -> str:
            m = s//60
            ss = s % 60
            hh = m//60
            mm = m % 60

            def fill_to_2(i: int) -> str:
                s = str(i)
                return s if len(s) == 2 else "0"*(2-len(s))+s
            return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"
        songData = []
        tData = []
        for i in data:
            pc = i["playCount"]
            t = i["song"]["dt"]//1000
            tt = pc*t
            tData.append(tt)
            songData.append(i)
        ts = tData.copy()
        ts.sort()
        for i in range(20):
            time = ts[-(i+1)]
            index = tData.index(time)
            song = songData[index]
            print(
                f"{i+1}: {song['song']['name']} || T:{second_format(song['song']['dt']//1000)} || C:{song['playCount']} || A:{second_format(time)}")
