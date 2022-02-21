import requests
from .urls import *
from .encrypt import NeteaseMusicEncrypt
from .user import NeteaseMusicConfigUser

class NeteaseMusicAnalyse:
    def __init__(self,config:NeteaseMusicConfigUser):
        requests.get(URL_USER_ANALYSE,headers=config.toHeader({}))
