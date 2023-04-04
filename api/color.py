from random import randint
from typing import Tuple

class Color:
    r: int
    g: int
    b: int

    def __init__(self, r:int, g:int, b:int) -> None:
        self.r = r
        self.g = g
        self.b = b

    def asTuple(self) -> Tuple[int,int,int]:
        return (self.r,self.g,self.b)    

    def asHex(self) -> str:
        return '#%02x%02x%02x' % (0, 128, 64)

    @staticmethod
    def randomColor():
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)

        return Color(r,g,b)    