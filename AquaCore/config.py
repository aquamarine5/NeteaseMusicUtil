from typing import Any, Dict


class BaseConfigUser:
    def __init__(self, id: int, isDefault: bool = False, **dt) -> None:
        self.id = id
        self.isDefault = isDefault
        self.isDefaultN = 1 if isDefault else 0
        self.data = dt

    @classmethod
    def createWithDict(cls, dt: Dict[str, Any]):
        b = cls()
        b.id = dt.pop("id")
        b.isDefault = dt.pop("isDefault")
        b.data = dt
        return b

    def __str__(self) -> str:
        return self.toUser()

    def toUser(self) -> str:
        raise NotImplementedError()

    def toDict(self) -> dict:
        b = self.data.copy()
        b["id"] = self.id
        b["isDefault"] = self.isDefault
        return b

    def toCookie(self) -> str:
        raise NotImplementedError()

    def toHeader(self, header: dict) -> dict:
        h = header.copy()
        h["Cookie"] = self.toCookie()
        return h


class BaseConfig:
    class NotLoginError(BaseException):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

        def __str__(self) -> str:
            return f"请先登录 使用account-login(或account-login-message)命令登录"

    class ConfigNotFoundError(BaseException):
        def __init__(self, id: int, *args: object) -> None:
            self.id = id
            super().__init__(*args)

        def __str__(self) -> str:
            return f"找不到id为{self.id}的用户"

    def __init__(self, file_path: str, data_type: type = BaseConfigUser) -> None:
        self.file_path = file_path
        self.type = data_type

    def login(self, data: BaseConfigUser):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            m = f.read()
            if m == "":
                f.write(str([data.toDict()]).replace("'",'"'))
            else:
                b: list = eval(m)
                i = [j["id"] for j in b]
                if data.id in i:
                    print("用户已记录，无需登录")
                    return
                f.seek(0)
                f.truncate()
                if data.isDefault:
                    b.insert(0, data.toDict())
                else:
                    b.append(data.toDict())
                f.write(str(b).replace("'",'"'))

    def get_default_config(self):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                raise self.NotLoginError()
            m: list = eval(r)
            if len(m) == 0:
                return self.NotLoginError()
            c:BaseConfigUser = self.type.createWithDict(m[0])
            return c

    def get_all_config(self):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                return []
            d = eval(r)
            return [self.type.createWithDict(i) for i in d]

    def get_all_config_cc(self):
        r = self.get_all_config()
        print("存储的所有账户: ")
        if r == []:
            print("没有任何账户")
        for i in range(len(r)):
            c: BaseConfigUser = r[i]
            print(i+1, '●' if c.isDefault else '○', c.toUser())

    def change_default_config(self, id: int):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                raise self.ConfigNotFoundError(id)
            e: list = eval(r)
            i = [j["id"] for j in e]
            e[0]["isDefault"] = 0
            if id not in i:
                raise self.ConfigNotFoundError(id)
            c = e[i.index(id)]
            e.remove(c)
            c["isDefault"] = 1
            e.insert(0, c)
            f.seek(0)
            f.truncate()
            f.write(str(e).replace("'",'"'))
            print(f"成功设置 {c['nickName']}({id}) 为新默认用户")

    def delete_config(self, id: int):
        with open(self.file_path, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                raise self.ConfigNotFoundError(id)
            e: list = eval(r)
            i = [j["id"] for j in e]
            if id not in i:
                raise self.ConfigNotFoundError(id)
            d = i.index(id)
            c = e[d]
            if c["isDefault"] == 1 and len(e) > 1:
                e[d+1]["isDefault"] = 1
            e.remove(c)
            f.seek(0)
            f.truncate()
            f.write(str(e).replace("'",'"'))
            print(f"成功删除id为 {id} 的用户")

    def get_config(self, id: int):
        d = self.get_all_config()
        i = [j.id for j in d]
        if id not in i:
            raise self.NotLoginError()
        return d[i.index(id)]

    def isLogin(self, id: int) -> bool:
        with open(self.file_path, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                return False
            d = eval(r)
            i = [j["id"] for j in d]
            return id in i
