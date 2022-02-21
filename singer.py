import requests

from bs4 import BeautifulSoup

from .AquaCore.progress import Progresser
from .song import NeteaseMusicSong
from .urls import *


class NeteaseMusicSinger:
    def __init__(self, id: int) -> None:
        self.url = URL_ARTIST_DETAIL % id
        self.bsoup = BeautifulSoup(requests.get(self.url,
                                                headers={
                                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}
                                                ).text, features="html.parser")

    def download_hotsong(self, path):
        m = self.bsoup.find(
            "div", attrs={"id": "song-list-pre-cache"}).find_all('li')
        p = Progresser(len(m))
        for i in m:
            p.print_slider_complex_animation_next()
            NeteaseMusicSong(int(i.find('a')['href'].split('=')[1])).download(
                f"{path}/{i.find('a').string}.mp3")

    @staticmethod
    def download_hotsong_cc(id: int, path: str = "."):
        NeteaseMusicSinger(id).download_hotsong(path)
