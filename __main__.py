from sys import argv

from .AquaCore.commandCompiler import EasyCommandCompiler
from .album import NeteaseMusicAlbum
from .config import NeteaseMusicConfig
from .encrypt import NeteaseMusicEncrypt
from .playlist import NeteaseMusicPlaylist
from .record import NeteaseMusicRecord
from .singer import NeteaseMusicSinger
from .song import NeteaseMusicSong
from .user import NeteaseMusicUser

if __name__ == "__main__":
    cc = EasyCommandCompiler({
        0: {
            "login": (NeteaseMusicUser.login, []),
            "sign": (NeteaseMusicUser.sign_cc, []),
            "analyse": (NeteaseMusicRecord.analyse_complex, []),
            "account-login": (NeteaseMusicUser.login, []),
            "account-login-qrcode": (NeteaseMusicUser.login, []),
            "account-all": (NeteaseMusicConfig.get_all_config_cc, []),
            "account-default": (NeteaseMusicConfig.get_default_config_cc, [])
        },
        1: {
            "encrypt": (NeteaseMusicEncrypt.neteaseMusicEncrypt_cc, [str]),
            "account-change": (NeteaseMusicConfig.change_default_config, [int]),
            "account-delete": (NeteaseMusicConfig.delete_config, [int]),
            "analyse": (NeteaseMusicRecord.analyse_cc, [str]),
            "alltime": (NeteaseMusicRecord.alltime_cc, [str]),
            "download": (NeteaseMusicSong.download_cc, [int]),
            "download-metadata": (NeteaseMusicSong.download_metadata_cc, [int]),
            "download-album": (NeteaseMusicAlbum.download_all_cc, [int]),
            "download-playlist": (NeteaseMusicPlaylist.download_all_cc, [int]),
            "downlaod-singer": (NeteaseMusicSinger.download_hotsong_cc, [int])
        },
        2: {
            "account-login-text": (NeteaseMusicUser.login_text, [int, str]),
            "download": (NeteaseMusicSong.download_cc, [int, str]),
            "download-metadata": (NeteaseMusicSong.download_metadata_cc, [int, str]),
            "download-album": (NeteaseMusicAlbum.download_all_cc, [int, str]),
            "download-playlist": (NeteaseMusicPlaylist.download_all_cc, [int, str]),
            "downlaod-singer": (NeteaseMusicSinger.download_hotsong_cc, [int, str])
        },
        3: {
            "account-add": (NeteaseMusicConfig.login_cc, [int, str, str])
        }
    }, '''
网易云音乐插件
Created by @aquamarine5(github.com/aquamarine5/AwesomeCore)
使用方法: 
在控制台输入
python neteaseMusic.py [后接函数名称] [参数,...]
目前可用的函数以及函数名称: 

sign - 签到
account-login - 同account-login-qrcode
account-login-qrcode - 使用二维码登录
account-login-text <phone:int> <password:str> - 使用账号 (手机号) 密码登录
account-add <id:int> <csrf:str> <musicu:str> - 添加账户 (仅用于测试阶段) 
account-default - 显示当前默认账户
account-all - 显示当前全部账户
account-change <id:int> - 更改默认账户
account-delete <id:int> - 删除账户
analyse - 整体分析
analyse <all/week> - 分析全部/本周数据
alltime <all/week> - 分析全部/这周听歌时长
download <id:int> [path:str] - 下载音乐
download-metadata <id:int> [path:str] - 下载音乐附带作者、专辑等元数据
download-album <id:int> [path:str] - 下载专辑全部音乐
download-playlist <id:int> [path:str] - 下载播放列表的全部音乐
download-singer <id:int> [path:str] - 下载歌手前五十音乐''')
    cc.compiled(argv)
