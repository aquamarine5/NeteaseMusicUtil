
from typing import Callable, Dict, List, Optional, Tuple, Type


class CommandArgument:
    def __init__(self, args: List[Type] = []) -> None:
        self.length = len(args)
        self.args = args


class CommandFunction:
    def __init__(self, function: Callable, arg: CommandArgument = CommandArgument([])) -> None:
        self.function = function
        self.arg = arg

    def run(self, args: Optional[List[str]]):
        a = self.arg.args
        r = (a[i](args[i]) for i in range(self.arg.length))
        self.function(*r)


class CommandCollection:
    def __init__(self, commandList: Dict[int, Dict[str, CommandFunction]], helpInfo: str = None) -> None:
        self.commandList = commandList
        self.helpInfo = helpInfo


class CommandCompiler:
    def __init__(self, commandList: Dict[int, Dict[str, CommandFunction]],
                 help: str = "", collection: Optional[List[CommandCollection]] = None) -> None:
        commandList[0]["help"] = CommandFunction(
            self.help, CommandArgument([]))
        self.commandList = commandList
        if collection != None:
            for i in collection:
                self.add_collection(i)
        self.helpInfo: str = help

    def add_collection(self, coll: CommandCollection):
        d = coll.commandList
        self.helpInfo+=coll.helpInfo
        for i in d:
            self.commandList[i].update(d[i])

    def compiled(self, cmd: List[str]):
        cl = self.commandList
        if len(cmd) == 1:
            self.help()
            return
        key = cmd[1]
        length = len(cmd)-2
        args = cmd[2:]
        if length not in cl:
            raise ValueError("找不到指定函数")
        else:
            if key not in cl[length]:
                raise ValueError("找不到指定函数")
            else:
                self.run(cl[length][key], args)

    def help(self):
        print(self.helpInfo)

    def run(self, cf: CommandFunction, args: List[str]):
        cf.run(args)


class EasyCommandCollection(CommandCollection):
    def __init__(self, commandList: Dict[int, Dict[str, Tuple[Callable, List[Type]]]], helpInfo: str = None) -> None:
        super().__init__(commandList,helpInfo)


class EasyCommandCompiler(CommandCompiler):
    def __init__(self, commandList: Dict[int, Dict[str, Tuple[Callable, List[Type]]]],
                 help: str = "", collection: Optional[List[EasyCommandCollection]] = None) -> None:
        commandList[0]["help"] = (self.help, [])
        self.commandList = commandList
        if collection != None:
            for i in collection:
                self.add_collection(i)
        self.helpInfo = help

    def add_collection(self, coll: EasyCommandCollection):
        super().add_collection(coll)

    def run(self, cf: Tuple[Callable, List[Type]], args: List[str]):
        r = (cf[1][i](args[i]) for i in range(len(args)))
        cf[0](*r)
