from .urls import *
from .webloader import NeteaseMusicWebLoader

class NeteaseMusicAlbum(NeteaseMusicWebLoader):
    def __init__(self,  id: int) -> None:
        super().__init__(URL_ALBUM_DETAIL, id)

    @staticmethod
    def download_all_cc(id: int, path: str = "."):
        return NeteaseMusicAlbum(id).download_all(path)
