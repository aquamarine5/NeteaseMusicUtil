import json
import sys
import requests
import re
import datetime
from .urls import *
from .encrypt import NeteaseMusicEncrypt
from .config import NeteaseMusicConfig, NeteaseMusicConfigBase, NeteaseMusicConfigUser


class NeteaseMusicAnalyse:
    def __init__(self, config: NeteaseMusicConfigUser, content=None, history=None) -> None:
        if content != None:
            self.content = content
            self.history = history
        else:
            self._created_by_web(config)

    def _created_by_web(self, config):
        c = requests.get(URL_ANALYSE_ANALYSE, headers=config.toHeader({})).text
        t = re.search(r"window.__INITIAL_DATA__ = ({.+})</script>", c).group(1)
        self.content = json.loads(t)

    def _load_type(self, d):
        self.analyse_typeUnion(d)
        # t=d['type']
        # if t==7: self.analyse_type7(d["data"])
        # elif t==1: self.analyse_type1(d["data"])

    def analyse(self, index: int = 0):
        d = self.content["reportFlowData"]["detail"][index]
        self._load_type(d)

    def load_analyse(self, d):
        self._load_type(d)

    def _load_othertype_data(self, d):
        if "otherType" in d:
            for i in d['otherType']:
                self._load_type(i)

    def _second_format(self, s: str) -> str:
        s = int(s)
        m = s//60
        ss = s % 60
        hh = m//60
        mm = m % 60

        def fill_to_2(i: int) -> str:
            s = str(i)
            return s if len(s) == 2 else "0"*(2-len(s))+s
        return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"

    def analyse_type1(self, d: dict):
        print(f"关键词: {d['keyword']}")
        print(f"这周听了 {d['listenSongs']} 首歌")
        print(
            f"听了 {d['listenWeekCount']} 次, 共 {self._second_format(d['listenWeekTime'])}")
        print("听歌时间表: ")
        for i in d['details']:
            print(
                f"    |{'-'*int(int(i['duration'])*2/60/60)}    {self._second_format(i['duration'])}")
        print(
            f"这周开始听的歌是: {d['startSong']['songName']} - {d['startSong']['artistNames']}")
        print(
            f"这周最后听的歌是: {d['endSong']['songName']} - {d['endSong']['artistNames']}")
        print(f"这周最喜欢的{len(d['favoriteSongs'])}首歌: ")
        for i in d['favoriteSongs']:
            print(f"    {i['songName']} - {i['artistNames']}")
        self._load_othertype_data(d)

    def analyse_typeUnion(self, d: dict):
        def c(data):
            return data in d and d[data] != None
        if(c('keyword')):
            print(f"关键词: {d['keyword']}")
        if(c('listenSongs')):
            print(f"这周听了 {d['listenSongs']}首歌")
        if(c('listenWeekCount')):
            print(
                f"听了 {d['listenWeekCount']} 次, 共 {self._second_format(d['listenWeekTime'])}")
        if(c('details')):
            print("听歌时间表: ")
            for i in d['details']:
                print(
                    f"    |{'-'*int(int(i['duration'])*2/60/60)}    {self._second_format(i['duration'])}")
        if(c('startSong')):
            print(
                f"这周开始听的歌是: {d['startSong']['songName']} - {d['startSong']['artistNames']}")
        if(c('endSong')):
            print(
                f"这周最后听的歌是: {d['endSong']['songName']} - {d['endSong']['artistNames']}")

        if(c('listenAlbumInfo')):
            print(f"听了 {d['listenAlbumInfo']['count']} 张专辑")
            for i in d["listenAlbumInfo"]["details"]:
                print(f"    {i['albumName']} 是你的{i['tag']}")
        if(c('listenCommonStyle')):
            print("听歌风格为: ")
            for i in d['listenCommonStyle']['styleDetailList']:
                print(
                    f"    {round(float(i['percent'])*100,1)}% 的{i['styleName']}")
        if(c("newPopularStyleName")):
            print(f"新听了{d['newPopularStyleName']}风格的歌")
        if(c('listenPlayer')):
            print(f"听了 {d['listenPlayer']['count']} 位歌手的歌")
            for i in d['listenPlayer']['players']:
                print(f"    {i['artistName']} 是你的{i['tag']}")
        if(c("newPlayer")):
            print(f"新听了{d['newPlayer']['artistName']}的歌")
        if(c("listenSingle")):
            print(f"听了 {d['listenSingle']['count']} 首歌")
            for i in d['listenSingle']['singles']:
                print(f"    {i['songName']} 是你的{i['tag']}")
            if("lyric" in d['listenSingle']):
                nn = "\n"  # avoid SyntaxError: f-string expression part cannot include a backslash
                print(f"    「{d['listenSingle']['lyric'].replace('@#',nn)}」")
        if(c('newSongs')):
            print("新听了: ")
            for i in d['newSongs']:
                print(f"    {i['songName']} - {i['artistNames']}")
        if(c('recommendPlayers')):
            print("推荐了以下歌手: ")
            for i in d['recommendPlayers']:
                print(f"    {i['artistName']}")
        if(c('musicEmotion')):
            print(f"听歌类型: {' '.join(d['musicEmotion']['subTitle'])}")
        # ignore d.musicEmotion.emotions
        # ignore d.musicYear.total
        if(c('musicYear')):
            print(
                f"你最常听 {d['musicYear']['year']}年的歌, 达到了{round(float(d['musicYear']['percent'])*100,1)}%")
            for i in d['musicYear']['yearPercents']:
                print(
                    f"    {i['startYear']}-{i['endYear']}的歌占你听歌的{round(float(i['percent'])*100,2)}%")
            for i in d['musicYear']['yearSingles']:
                print(f"    {i['songName']}是{i['tag']}")
        if(c('song')):
            print(
                f"您的这周歌曲是: {d['song']['songName']}, {d['subTitle'].replace('##1','')}")
            if(c("songInfos")):
                print("其次还有: ")
        if(c("songInfos")):
            for i in d['songInfos']:
                print(f"    {i['songName']} - {i['artistNames']}")
        if(c('favoriteSongs')):
            print(f"这周最喜欢的{len(d['favoriteSongs'])}首歌: ")
            for i in d['favoriteSongs']:
                print(f"    {i['songName']} - {i['artistNames']}")
        if(c('favoritePlayers')):
            print(f"这周最喜欢的{len(d['favoritePlayers'])}的歌手: ")
            for i in d['favoritePlayers']:
                print(f"    {i['artistName']}")
        self._load_othertype_data(d)

    def analyse_type4(self, d: dict):
        print(f"关键词: {d['keyword']}")
        print(f"这周听了 {d['listenSongs']}首歌")
        print(
            f"听了 {d['listenWeekCount']} 次, 共 {self._second_format(d['listenWeekTime'])}")
        # ignore d.listenStyleSongs
        print(f"这周的听歌风格是 {d['styleName']}")
        for i in d['secondStyleDataList']:
            print(f"    {i['name']}: {i['song']['songName']}")
        print("这周常听的歌有: ")
        for i in d['songInfos']:
            print(f"    {i['songName']} - {i['artistNames']}")

    def analyse_type7(self, d: dict):
        print(f"关键词: {d['keyword']}")
        print(f"这周听了 {d['listenSongs']}首歌")
        print(
            f"听了 {d['listenWeekCount']} 次, 共 {self._second_format(d['listenWeekTime'])}")
        print(f"听了 {d['listenAlbumInfo']['count']} 张专辑")
        for i in d["listenAlbumInfo"]["details"]:
            print(f"    {i['albumName']} 是你的{i['tag']}")
        print("听歌风格为: ")
        for i in d['listenCommonStyle']['styleDetailList']:
            print(f"    {round(float(i['percent'])*100,1)}% 的{i['styleName']}")
        print(f"听了 {d['listenPlayer']['count']} 位歌手的歌")
        for i in d['listenPlayer']['players']:
            print(f"    {i['artistName']} 是你的{i['tag']}")
        print(f"听了 {d['listenSingle']['count']} 首歌")
        for i in d['listenSingle']['singles']:
            print(f"    {i['songName']} 是你的{i['tag']}")
        if("lyric" in d['listenSingle']):
            nn = "\n"  # avoid SyntaxError: f-string expression part cannot include a backslash
            print(f"    「{d['listenSingle']['lyric'].replace('@#',nn)}」")
        print(f"听歌类型: {' '.join(d['musicEmotion']['subTitle'])}")
        # ignore d.musicEmotion.emotions
        # ignore d.musicYear.total
        print(
            f"你最常听 {d['musicYear']['year']}年的歌, 达到了{round(float(d['musicYear']['percent'])*100,1)}%")
        for i in d['musicYear']['yearPercents']:
            print(
                f"    {i['startYear']}-{i['endYear']}的歌占你听歌的{round(float(i['percent'])*100,2)}%")
        for i in d['musicYear']['yearSingles']:
            print(f"    {i['songName']}是{i['tag']}")
        print(
            f"您的这周歌曲是: {d['song']['songName']}, {d['subTitle'].replace('##1','')}")
        print("其次还有: ")
        for i in d['songInfos']:
            print(f"    {i['songName']} - {i['artistNames']}")
        self._load_othertype_data(d)


class NeteaseMusicHistoryAnalyse():
    def __init__(self, year: int, month: int) -> None:
        monthstart = datetime.datetime(year, month, 1, 0, 0, 0)
        monthend = datetime.datetime(year, month+1, 1, 0, 0, 0)
        monthend -= datetime.timedelta(0, 1)
        s = str(monthstart.timestamp()).replace('.0', '000')
        e = str(monthend.timestamp()).replace('.0', '999')
        print(str({
            "userId": "",
            "startTime": int(s),
            "endTime": int(e),
            "limit": 10,
            "type": 1,
            "csrf_token": NeteaseMusicConfig.get_default_config().csrf
        }).replace("'", '"'))
        self.data = NeteaseMusicEncrypt.neteaseMusicPost(URL_ANALYSE_WEEKFLOW, str({
            "endTime": int(e), 
            "limit": 10, 
            "startTime": int(s), 
            "type": 1,
            "userId": "",
            "csrf_token": NeteaseMusicConfig.get_default_config().csrf
        }).replace("'", '"'), referer="https://music.163.com/prime/m/viptimemachine")

    def analyse(self, week: int):
        print(self.data)
        NeteaseMusicAnalyse(None, content=self.data, history=self).load_analyse(
            self.data['data']['details'][week])

    def _if_available_query(year: int, month: int):
        c = NeteaseMusicEncrypt.neteaseMusicPost(
            URL_ANALYSE_HISTORY, {"userId": ""})
        for i in c['data']:
            if year == i['year']:
                if month in i['month']:
                    return True
        return False

    @staticmethod
    def get_histroy_show():
        c = NeteaseMusicEncrypt.neteaseMusicPost(
            URL_ANALYSE_HISTORY, {"userId": ""})
        print("可支持查询以下数据: ")
        for i in c["data"]:
            t = f"{i['year']}年: "
            for j in i['month']:
                t += f"{j} "
            print(t)


if __name__ == "__main__":
    if "qavailable" in sys.argv:
        NeteaseMusicHistoryAnalyse.get_histroy_show()
    if len(sys.argv) == 4:
        NeteaseMusicHistoryAnalyse(int(sys.argv[1]), int(
            sys.argv[2])).analyse(sys.argv[3])
    else:
        NeteaseMusicAnalyse(NeteaseMusicConfig.get_default_config()).analyse()
