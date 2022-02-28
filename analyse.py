import json
import requests,re,time
from .urls import *
from .encrypt import NeteaseMusicEncrypt
from .config import NeteaseMusicConfig, NeteaseMusicConfigBase, NeteaseMusicConfigUser

class NeteaseMusicAnalyse:
    def __init__(self,config:NeteaseMusicConfigUser):
        c=requests.get(URL_USER_ANALYSE,headers=config.toHeader({})).text
        t=re.search(r"window.__INITIAL_DATA__ = ({.+})</script>",c).group(1)
        self.content=json.loads(t)
    def _load_type(self,d):
        t=d['type']
        if t==7: self.analyse_type7(d)
    def analyse(self,index:int=0):
        print(self.content)
        d=self.content["reportFlowData"]["detail"][index]
        self._load_type(d)
    def _load_othertype_data(self,d):
        if "otherType" in d:
            for i in d['otherType']:
                self._load_type(i)
    def analyse_type7(self,d:dict):
        print(f"关键词: {d['keyword']}")
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
            nn="\n" # avoid SyntaxError: f-string expression part cannot include a backslash
            print(f"    「{d['listenSingle']['lyric'].replace('@#',nn)}」")
        print(f"听歌类型: {' '.join(d['musicEmotion']['subTitle'])}")
        # ignore d.musicEmotion.emotions
        # ignore d.musicYear.total
        print(f"你最常听 {d['musicYear']['year']}年的歌, 达到了{round(float(d['musicYear']['percent'])*100,1)}%")
        for i in d['musicYear']['yearPercents']:
            print(f"    {i['startYear']}-{i['endYear']}的歌占你听歌的{round(float(i['percent'])*100,2)}%")
        for i in d['musicYear']['yearSingles']:
            print(f"    {i['songName']}是{i['tag']}")
        print(f"您的这周歌曲是: {d['song']['songName']}, {d['subTitle'].replace('##1','')}")
        print("其次还有: ")
        for i in d['songInfos']:
            print(f"    {i['songName']} - {i['artistNames']}")
if __name__=="__main__":
    NeteaseMusicAnalyse(NeteaseMusicConfig.get_default_config()).analyse()
        
