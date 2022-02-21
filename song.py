
from typing import Union

import requests
from mutagen import id3

from .album import *
from .config import *
from .encrypt import NeteaseMusicEncrypt
from .singer import NeteaseMusicSinger
from .urls import *


class NeteaseMusicSong:
    def __init__(self, id: int) -> None:
        self.id = id
        self.isVip = self.url is None
        v = self.get_music_detail(id)
        if v["code"] == -460:
            v = None
            print("获取详情失败")
            return
        else:
            if v["songs"] == []:
                raise ValueError("找不到歌曲")
        self.infos = v["songs"]
        self.info = v["songs"][0]
        self.name = self.info["name"]
        self.picUrl = self.info["album"]["picUrl"]
        self.album = NeteaseMusicAlbum(self.info["album"]["id"])
        self.artists = [NeteaseMusicSinger(i["id"])
                        for i in self.info["artists"]]
        self.artistsName = "/".join([i["name"] for i in self.info["artists"]])

    @property
    def url(self) -> str:
        return NeteaseMusicSong.get_music_url(self.id)["data"][0]["url"]

    @property
    def music_webplayer(self):
        return NeteaseMusicSong.get_music_url_v1(self.id)

    @property
    def music_iframe(self) -> str:
        return NeteaseMusicSong.get_music_url(self.id)

    @property
    def detail(self) -> str:
        return NeteaseMusicSong.get_music_detail(self.id)
    #######################################

    @staticmethod
    def get_music_detail(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"id": id, "ids": f'["{id}"]', "limit": 10000,
                 "offset": 0, "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicEncrypt.neteaseMusicPost(URL_SONG_DETAIL, c) if isPost else NeteaseMusicEncrypt.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "br": 128000,
                 "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicEncrypt.neteaseMusicPost(URL_SONG_DATA, c) if isPost else NeteaseMusicEncrypt.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url_v1(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "level": "standard", "encodeType": "mp3"})
        return NeteaseMusicEncrypt.neteaseMusicPost(URL_SONG_DATA_V1, c) if isPost else NeteaseMusicEncrypt.neteaseMusicEncrypt(c)

    @staticmethod
    def download_cc(id, path="./Download.mp3"):
        NeteaseMusicSong(id).download(path)

    @staticmethod
    def download_metadata_cc(id, path="./Download.mp3"):
        NeteaseMusicSong(id).download_with_metadata(path)

    def download(self, path):
        if self.isVip:
            print(f"\n{self.id}({self.id})不能下载")
            return
        with open(path, "wb+") as f:
            f.write(requests.get(self.url).content)

    def download_with_metadata(self, path, includeImage: bool = True):
        if self.isVip:
            print(f"\n{self.id}({self.id})不能下载")
            return
        with open(path, "wb+") as f:
            f.write(requests.get(self.url).content)
        f = id3.ID3(path)
        f.update_to_v24()
        f["TPE1"] = id3.TPE1(encoding=3, text=self.artistsName)
        f["WOAR"] = id3.WOAR(
            encoding=3, url=f"https://music.163.com/song?id={self.id}")
        f["TALB"] = id3.TALB(encoding=3, text=self.info["album"]["name"])
        f["TIT2"] = id3.TIT2(encoding=3, text=self.name)
        if includeImage:
            f["APIC"] = id3.APIC(encoding=3, mime="image/jpeg", type=3, desc=u"cover",
                                 data=requests.get(f"{self.picUrl}?param=256y256").content)
        f.save()
