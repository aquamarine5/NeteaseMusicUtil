import requests
import urllib.parse
from base64 import b64encode
from Crypto.Cipher import AES
from .urls import *
class NeteaseMusicEncrypt:
    @staticmethod
    def neteaseMusicEncrypt(content: str) -> str:
        def AES_encrypt(key: str, message: str) -> bytes:
            def a16(text):
                padding = 16 - len(text) % 16
                text = text.decode('utf-8')
                text += padding * chr(padding)
                return text.encode('utf-8')
            a = AES.new(key, AES.MODE_CBC, iv=b'0102030405060708')
            return b64encode(a.encrypt(a16(message)))
        asrsea0 = content
        asrsea3 = "0CoJUm6Qyw8W8jud"
        a_c = "GvuqQ2m9sizBbmo4"
        p = AES_encrypt(asrsea3.encode('utf-8'), asrsea0.encode('utf-8'))
        params = AES_encrypt(a_c.encode('utf-8'), p).decode('utf-8')
        return params

    @staticmethod
    def neteaseMusicEncrypt_cc(content: str):
        print(NeteaseMusicEncrypt.neteaseMusicEncrypt(content))

    @classmethod
    def neteaseMusicPost(cls, url: str, content: str, cookies=None) -> dict:
        m = cls.neteaseMusicEncrypt(content)
        h = header.copy()
        if cookies != None:
            h["Cookie"] = cookies
        v = requests.post(
            url, cls.join(m), headers=h).json()
        return v

    @staticmethod
    def join(params: str, encsecKey: str = encSecKey) -> str:
        return f"params={urllib.parse.quote(params)}&encSecKey={urllib.parse.quote(encsecKey)}"