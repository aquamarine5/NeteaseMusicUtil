
from typing import Union, Tuple
from time import time


class Progresser():
    def __init__(self, length: int) -> None:
        self.length: int = length
        self.progress = 0
        self.lastTime = 0
        self.startTime = 0
        self.speed = 0

    def get_progress(self, p: Union[float, int]) -> float:
        return p/(self.length)

    def get_slider(self, p: Union[float, int],
                   filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10) -> str:
        progress: float = self.get_progress(p)
        filled_count = int(progress*slider_length)
        if filled_count >= slider_length:
            filled_count = slider_length
        return f'{filled_border[0]}{filled_str*filled_count}{filled_none*(slider_length-filled_count)}{filled_border[1]}'

    def get_slider_complex(self, p: Union[float, int],
                           show_count: bool = True, show_progress: bool = True,
                           filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10) -> str:
        slider: str = self.get_slider(
            p, filled_str, filled_border, filled_none, slider_length)
        if show_count:
            slider += f' ({p}/{self.length})'
        if show_progress:
            slider += f' {int(self.get_progress(p)*100)}%'
        return slider

    def pslider(self, p: Union[float, int],
                filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10):
        print(self.get_slider(p, filled_str,
                              filled_border, filled_none, slider_length))

    def pslider_animation(self, p: Union[float, int],
                          filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10):
        print(self.get_slider(p, filled_str, filled_border,
                              filled_none, slider_length), end="\r")

    def pslider_complex(self, p: Union[float, int],
                        show_count: bool = True, show_progress: bool = True,
                        filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10):
        print(self.get_slider_complex(p, show_count, show_progress,
                                      filled_str, filled_border, filled_none, slider_length))

    def pslider_complex_animation(self, p: Union[float, int],
                                  show_count: bool = True, show_progress: bool = True,
                                  filled_str: str = "-", filled_border: Tuple[str, str] = ["[", "]"], filled_none: str = " ", slider_length: int = 10):
        print(self.get_slider_complex(p, show_count, show_progress,
                                      filled_str, filled_border, filled_none, slider_length), end="\r")

    def print_slider_complex_animation_next(self):
        self.progress += 1
        if self.lastTime == 0:
            self.startTime = time()
            self.lastTime = time()
        else:
            offset = time()-self.lastTime
            if self.speed == 0:
                self.speed = offset
            else:
                self.speed = (self.speed*self.progress -
                              1+offset)/(self.progress)
        eta = second2string(float(self.length-self.progress)*float(self.speed))

        print(self.get_slider_complex(self.progress)+"  ETA: "+eta, end="\r")

    def show_run_time(self):
        print(f"\nUse {round(time()-self.startTime,4)}s to run.")

class ValuedProgresser():
    def __init__(self, slider_length: int = 10,filled_str: str = "-", filled_none: str = " ") -> None:
        self.slider_length=slider_length
        self.p=0
        self.filled_str=filled_str
        self.filled_none=filled_none
    def get_slider_inside(self):
        l=[self.filled_none for _ in range(self.slider_length-1)]
        l.insert(self.p,self.filled_str)
        self.p+=1
        if self.p>=self.slider_length:
            self.p=0
        return "".join(l)
    def pslider_animation_next(self,value:int, filled_border: Tuple[str, str] = ["[", "]"]):
        print(f'{filled_border[0]}{self.get_slider_inside()}{filled_border[1]} ({value})',end="\r")
def second2string(s: int) -> str:
    m = 0
    h = 0
    if s >= 60:
        s = int(s-(m := s//60)*60)
    if m >= 60:
        m = int(m-(h := m//60)*60)
    if (ss := str(s)) == "0":
        ss = "00"
    if (hh := str(h)) == "0":
        hh = "00"
    if (mm := str(m)) == "0":
        mm = "00"
    return f"{hh}:{mm}:{ss}"
