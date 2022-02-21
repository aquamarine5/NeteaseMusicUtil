import requests
from bs4 import BeautifulSoup

from .AquaCore.progress import Progresser
from .song import *
from .urls import *


class NeteaseMusicWebLoader:
    def __init__(self, baseUrl: str, id: int) -> None:
        self.data = BeautifulSoup(requests.get(
            baseUrl % id, headers=header).text, features="html.parser").find("div", id="song-list-pre-cache")

    def download_all(self, path: str):
        d = self.data.find_all("li")
        p = Progresser(len(d))
        for i in d:
            a = i.a
            name = a.string
            id = int(a["href"].split("=")[1])
            NeteaseMusicSong(id).download(path+f"/{name}.mp3")
            p.print_slider_complex_animation_next()
