from .urls import *
from .webloader import NeteaseMusicWebLoader
class NeteaseMusicPlaylist(NeteaseMusicWebLoader):
    def __init__(self,  id: int) -> None:
        super().__init__(URL_PLAYLIST_DETAIL, id)

    @staticmethod
    def download_all_cc(id: int, path: str = "."):
        return NeteaseMusicPlaylist(id).download_all(path)

