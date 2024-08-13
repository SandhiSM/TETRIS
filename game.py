import keyboard
import json
import os
import random
import threading
import time

sleep = lambda: time.sleep(0.2)

class Minos:
    def __init__(self, shape: str) -> None:
        self.shape: str = shape
        self.x: int = 4 if shape in {"O", "Z"} else 3
        self.depth: int = 0
        self.rotated: int = 0
        self.left: bool = False
        self.right: bool = False
        self.down: bool = False
        self.rotate: bool = False
        self.deploy()
        return

    def deploy(self, remove: bool=False) -> None:
        char: str = " " if remove else "="
        match self.rotated:
            case 0:
                match self.shape:
                    case "I":
                        for i in range(4):
                            stage[self.depth][self.x+i] = char
                    case "O":
                        for i in range(2):
                            for j in range(2):
                                stage[self.depth+i][self.x+j] = char
                    case "T":
                        stage[self.depth][self.x+1] = char
                        for i in range(3):
                            stage[self.depth+1][self.x+i] = char
                    case "S":
                        for i in range(2):
                            for j in range(2):
                                stage[self.depth+i][self.x-i+j+1] = char
                    case "Z":
                        for i in range(2):
                            for j in range(2):
                                stage[self.depth+i][self.x+i+j] = char
                    case "J":
                        stage[self.depth][self.x] = char
                        for i in range(3):
                            stage[self.depth+1][self.x+i] = char
                    case "L":
                        stage[self.depth][self.x+2] = char
                        for i in range(3):
                            stage[self.depth+1][self.x+i] = char
            case 1:
                match self.shape:
                    case "I":
                        for i in range(4):
                            stage[self.depth+i][self.x] = char
                    case "T":
                        stage[self.depth+1][self.x+1] = char
                        for i in range(3):
                            stage[self.depth+i][self.x] = char
                    case "S":
                        for i in range(2):
                            for j in range(2):
                                stage[self.depth+i+j][self.x+i] = char
                    case "Z":
                        for i in range(2):
                            for j in range(2):
                                stage[self.depth-i+j+1][self.x+i] = char
                    case "J":
                        stage[self.depth][self.x+1] = char
                        for i in range(3):
                            stage[self.depth+i][self.x] = char
                    case "L":
                        stage[self.depth+2][self.x+1] = char
                        for i in range(3):
                            stage[self.depth+i][self.x] = char
            case 2:
                match self.shape:
                    case "T":
                        stage[self.depth+1][self.x+1] = char
                        for i in range(3):
                            stage[self.depth][self.x+i] = char
                    case "J":
                        stage[self.depth+1][self.x+2] = char
                        for i in range(3):
                            stage[self.depth][self.x+i] = char
                    case "L":
                        stage[self.depth+1][self.x] = char
                        for i in range(3):
                            stage[self.depth][self.x+i] = char
            case 3:
                match self.shape:
                    case "T":
                        stage[self.depth+1][self.x] = char
                        for i in range(3):
                            stage[self.depth+i][self.x+1] = char
                    case "J":
                        stage[self.depth+2][self.x] = char
                        for i in range(3):
                            stage[self.depth+i][self.x+1] = char
                    case "L":
                        stage[self.depth][self.x] = char
                        for i in range(3):
                            stage[self.depth+i][self.x+1] = char
        return

    def move(self, direction: str) -> None: # 動かせるという前提の下で実行する
        match direction:
            case "left":
                self.deploy(remove=True)
                self.x -= 1
                self.deploy()
            case "right":
                self.deploy(remove=True)
                self.x += 1
                self.deploy()
            case "rotate": # もっと条件設定が必要
                self.deploy(remove=True)
                if self.shape in {"I", "S", "Z"}:
                    self.rotated += 1 if self.rotated == 0 else -1
                else:
                    self.rotated += 1 if self.rotated != 3 else -3
                self.deploy()
            case "down":
                self.deploy(remove=True)
                self.depth += 1
                self.deploy()
        return

    def drop(self) -> None:
        while not self.down:
            self.move("down")
            self.flag()
        return

    def flag(self) -> None:
        match self.rotated:
            case 0:
                match self.shape:
                    case "I":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else False
                        self.right = True if (self.x+3) == 9 else True if stage[self.depth][self.x+4] == "=" else False
                        if self.depth == 19:
                            self.down = True
                        else:
                            for i in range(4):
                                if stage[self.depth+1][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        if self.depth >= 17:
                            self.rotate = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i+1][self.x] == "=":
                                    self.rotate = True
                                    break
                            else:
                                self.rotate = False
                    case "O":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(2):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        if (self.x+2) == 10 :
                            self.right = True
                        else:
                            for i in range(2):
                                if stage[self.depth+i][self.x+2] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        if (self.depth+1) == 19:
                            self.down = True
                        else:
                            for i in range(2):
                                if stage[self.depth+2][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True
                    case "T":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x-1] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+2] == "=" else True if stage[self.depth+1][self.x+3] == "=" else False
                        if (self.depth+1) == 19:
                            self.down = True
                        else:
                            for i in range(3):
                                if stage[self.depth+2][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                    case "S":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x-1] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+3] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                        if ((self.depth+1) == 19) | (stage[self.depth+1][self.x+2] == "="):
                            self.down = True
                        else:
                            for i in range(2):
                                if stage[self.depth+2][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                    case "Z":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+2] == "=" else True if stage[self.depth+1][self.x+3] == "=" else False
                        if ((self.depth+1) == 19) | (stage[self.depth+1][self.x] == "="):
                            self.down = True
                        else:
                            for i in range(2):
                                if stage[self.depth+2][self.x+i+1 ] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                    case "J":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x-1] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+1][self.x+3] == "=" else False
                        if (self.depth+1) == 19:
                            self.down = True
                        else:
                            for i in range(3):
                                if stage[self.depth+2][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                    case "L":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+1][self.x-1] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+3] == "=" else True if stage[self.depth+1][self.x+3] == "=" else False
                        if (self.depth+1) == 19:
                            self.down = True
                        else:
                            for i in range(3):
                                if stage[self.depth+2][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+2][self.x] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
            case 1:
                match self.shape:
                    case "I":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(4):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        if (self.x+1) == 10:
                            self.right = True
                        else:
                            for i in range(4):
                                if stage[self.depth+i][self.x+1] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        self.down = True if (self.depth+4) == 20  else True if stage[self.depth+4][self.x] == "=" else False
                        if self.x >= 7:
                            self.rotate = True
                        else:
                            for i in range(3):
                                if stage[self.depth][self.x+i+1] == "=":
                                    self.rotate = True
                                    break
                            else:
                                self.rotate = False
                    case "T":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        self.right = True if (self.x+1) == 9 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+1][self.x+2] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+3][self.x] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth][self.x+2] == "=" else False
                    case "S":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x-1] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                        self.right = True if (self.x+1) == 9 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+1][self.x+2] == "=" else True if stage[self.depth+2][self.x+2] == "=" else False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+2][self.x] == "=" else True if stage[self.depth+3][self.x+1] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth][self.x+2] == "=" else False
                    case "Z":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x-1] == "=" else True if stage[self.depth+2][self.x-1] == "=" else False
                        self.right = True if (self.x+1) == 9 else True if stage[self.depth][self.x+2] == "=" else True if stage[self.depth+1][self.x+2] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+3][self.x] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                    case "J":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        self.right = True if (self.x+1) == 9 else True if stage[self.depth][self.x+2] == "=" else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+3][self.x] == "=" else True if stage[self.depth+1][self.x+1] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x+2] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                    case "L":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        self.right = True if (self.x+1) == 9 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+2][self.x+2] == "=" else False
                        if (self.depth+2) == 19:
                            self.down = True
                        else:
                            for i in range(2):
                                if stage[self.depth+3][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x+1] == "=" else True if stage[self.depth][self.x+2] == "=" else False
            case 2:
                match self.shape:
                    case "T":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x] == "=" else False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+3] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                        self.down = True if (self.depth+1) == 19 else True if stage[self.depth+2][self.x+1] == "=" else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
                    case "J":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x+1] == "=" else False
                        if (self.x+2) == 9:
                            self.right = True
                        else:
                            for i in range(2):
                                if stage[self.depth+i][self.x+3] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        self.down = True if (self.depth+1) == 19 else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+2][self.x+2] == "=" else False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+2][self.x+1] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                    case "L":
                        if self.x == 0:
                            self.left = True
                        else:
                            for i in range(2):
                                if stage[self.depth+i][self.x-1] == "=":
                                    self.left = True
                                    break
                            else:
                                self.left = False
                        self.right = True if (self.x+2) == 9 else True if stage[self.depth][self.x+3] == "=" else True if stage[self.depth+1][self.x+1] == "=" else False
                        self.down = True if (self.depth+1) == 19 else True if stage[self.depth+2][self.x] == "=" else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                        self.rotate = True if self.depth >= 18 else True if stage[self.depth+1][self.x+1] == "=" else True if stage[self.depth+2][self.x+1] == "=" else False
            case 3:
                match self.shape:
                    case "T":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x-1] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                        if (self.x+1) == 9:
                            self.right = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x+2] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+3][self.x+1] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth+1][self.x+2] == "=" else False
                    case "J":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+2][self.x-1] == "=" else False
                        if (self.x+1) == 9:
                            self.right = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x+2] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        if (self.depth+2) == 19:
                            self.down = True
                        else:
                            for i in range(2):
                                if stage[self.depth+3][self.x+i] == "=":
                                    self.down = True
                                    break
                            else:
                                self.down = False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth][self.x] == "=" else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+1][self.x+2] == "=" else False
                    case "L":
                        self.left = True if self.x == 0 else True if stage[self.depth][self.x-1] == "=" else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+2][self.x] == "=" else False
                        if (self.x+1) == 9:
                            self.right = True
                        else:
                            for i in range(3):
                                if stage[self.depth+i][self.x+2] == "=":
                                    self.right = True
                                    break
                            else:
                                self.right = False
                        self.down = True if (self.depth+2) == 19 else True if stage[self.depth+3][self.x+1] == "=" else True if stage[self.depth+1][self.x] == "=" else False
                        self.rotate = True if self.x >= 8 else True if stage[self.depth+1][self.x] == "=" else True if stage[self.depth+1][self.x+2] == "=" else True if stage[self.depth][self.x+2] == "=" else False
        return

stage: list[list[str]] = [
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
]
DELIMITER: str = " "*10 + "-"*6
SPACE: str = " "*9 + "|" + " "*6 + "|"
I: str = " "*9 + "| " + "="*4 + " |"
O: str = " "*9 + "|  " + "="*2 + "  |"
T0: str = " "*9 + "|  " + "=" + "   |"
T1: str = " "*9 + "| " + "="*3 + "  |"
S0: str = " "*9 + "|  " + "="*2 + "  |"
S1: str = " "*9 + "| " + "="*2 + "   |"
Z0: str = " "*9 + "| " + "="*2 + "   |"
Z1: str = " "*9 + "|  " + "="*2 + "  |"
J0: str = " "*9 + "| " + "=" + "    |"
J1: str = " "*9 + "| " + "="*3 + "  |"
L0: str = " "*9 + "|   " + "=" + "  |"
L1: str = " "*9 + "| " + "="*3 + "  |"

def game() -> None:
    global stage
    def key_input():
        nonlocal mino, hold, pause, alive, paused
        flag = lambda: mino.flag()
        while alive:
            match keyboard.read_key():
                case "left":
                    flag()
                    if not mino.left:
                        mino.move("left")
                        flag()
                        print_stage()
                        sleep()
                case "right":
                    flag()
                    if not mino.right:
                        mino.move("right")
                        flag()
                        print_stage()
                        sleep()
                case "up":
                    flag()
                    if not mino.rotate:
                        mino.move("rotate")
                        flag()
                        print_stage()
                        sleep()
                case "down":
                    mino.drop()
                    print_stage()
                    sleep()
                case "space":
                    hold = mino.shape
                    # 今後いろいろ実装
                case "esc":
                    pause = True
                    paused = True
                    print_stage()
                    sleep()
                    while pause:
                        match keyboard.read_key():
                            case "esc":
                                pause = False
                                sleep()
                                break
                            case "q":
                                pause = False
                                alive = False
                                break

    def line() -> None:
        nonlocal point, level
        row: int = 0
        for i in range(20):
            if " " not in stage[i]:
                row += 1
                stage.pop(i)
                stage.insert(0, [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "])
                point += (level * 100) * row if level != 0 else 100
                if level != 19:
                    level += 1 if point % 1000 == 0 else 0
        return

    def print_stage() -> None:
        os.system("cls")
        print("-"*25)
        for (i, s) in enumerate(stage, 0):
            print("|< " + " ".join(s) + " >|", end="")
            match i:
                case 1:
                    print(" "*8 + f"P O I N T: {point}")
                case 3:
                    print(" "*8 + f"L E V E L: {level}")
                case 5:
                    print(" "*8 + "H O L D")
                case 6:
                    print(DELIMITER)
                case 7:
                    match hold:
                        case "I":
                            print(I)
                        case "O":
                            print(O)
                        case "T":
                            print(T0)
                        case "S":
                            print(S0)
                        case "Z":
                            print(Z0)
                        case "J":
                            print(J0)
                        case "L":
                            print(L0)
                        case "N":
                            print(SPACE)
                case 8:
                    match hold:
                        case "I":
                            print(DELIMITER)
                        case "O":
                            print(O)
                        case "T":
                            print(T1)
                        case "S":
                            print(S1)
                        case "Z":
                            print(Z1)
                        case "J":
                            print(J1)
                        case "L":
                            print(L1)
                        case "N":
                            print(SPACE)
                case 9:
                    print(DELIMITER) if hold != "I" else print()
                case 11:
                    print(" "*8 + "N E X T")
                case 12:
                    print(DELIMITER)
                case 13:
                    match shapes[index+1] if index != 6 else shapes[0]:
                        case "I":
                            print(I)
                        case "O":
                            print(O)
                        case "T":
                            print(T0)
                        case "S":
                            print(S0)
                        case "Z":
                            print(Z0)
                        case "J":
                            print(J0)
                        case "L":
                            print(L0)
                case 14:
                    match shapes[index+1] if index != 6 else shapes[0]:
                        case "I":
                            print(DELIMITER)
                        case "O":
                            print(O)
                        case "T":
                            print(T1)
                        case "S":
                            print(S1)
                        case "Z":
                            print(Z1)
                        case "J":
                            print(J1)
                        case "L":
                            print(L1)
                case 15:
                    match shapes[index+1] if index != 6 else shapes[0]:
                        case "I":
                            print()
                        case _:
                            print(DELIMITER)
                case 17:
                    print(" "*8 + "P A U S E") if pause else print()
                case 18:
                    print(" "*8 + "P R E S S  E S C  K E Y  T O  R E S U M E") if pause else print()
                case 19:
                    print(" "*8 + "P R E S S  Q  K E Y  T O  Q U I T") if pause else print()
                case _:
                    print()
        print("-"*25)
        return

    def save() -> None:
        data: list[dict[str:str]] = file("read")
        data.append({"date": f"{time.strftime("%Y-%m-%d %H:%M:%S")}", "point": point})
        file("write", data)

    shapes: list[str] = ["I", "O", "T", "S", "Z", "J", "L"]
    point: float = 0.0
    level: int = 0
    index: int = 0
    hold: str = "N" # (I, O, T, S, Z, J, L, N(=None)) おいおい実装
    alive: bool = True
    pause: bool = False
    paused: bool= False
    stage = [
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
]
    key = threading.Thread(target=key_input, daemon=True)
    key.start()
    while True:
        random.shuffle(shapes) if index == 0 else None
        print_stage()
        mino: Minos = Minos(shapes[index])
        line()
        mino.flag()
        if mino.down:
            alive = False
            print_stage()
            save() if not paused else None
            break
        while (not mino.down) & alive:
            print_stage()
            time.sleep(2 - level * 0.1) # 落下速度がここで変わる
            mino.move("down") if (not mino.down) & (not pause) else None
            mino.flag()
        line()
        print_stage()
        index += 1 if index != 6 else -6
        sleep()
    key.join()
    return

def result(game: bool=False) -> None:
    os.system("cls")
    data: list[dict[str:str]] = file("read")
    if data == []:
        print("- - -  N O  D A T A  - - -")
    else:
        print("- - - G A M E  O V E R  - - -") if game else None
        print("- - -  R E S U L T  - - -\n")
        for d in data:
            print(f"{d["date"]}: {d["point"]}")
    print("\n[P R E S S  E S C  K E Y  T O  R E T U R N]")
    while True:
        if keyboard.read_key() == "esc":
            break
    return

def operation() -> None:
    os.system("cls")
    print("""
- - -  H O W  T O  P L A Y  T H I S  G A M E  - - -

LEFT AND RIGHT ARROW KEY: MOVE MINO
          DOWN ARROW KEY: DROP MINO (HARD DROP)
            UP ARROW KEY: ROTATE MINO
               SPACE KEY: HOLD MINO (NOT IMPLEMENTED)
                 ESC KEY: PAUSE GAME

[E S C  K E Y  T O  R E T U R N]
""")
    while True:
        if keyboard.read_key() == "esc":
            break
    return

selector: list[str] = [">", " ", " ", " "]

def main() -> None:
    def print_start() -> None:
        os.system("cls")
        print(f"""
TETRIS

[{selector[0]}] P L A Y
[{selector[1]}] R E S U L T
[{selector[2]}] O P E R A T I O N
[{selector[3]}] Q U I T
""")
        return
    print_start()
    while True:
        current: int = selector.index(">")
        match keyboard.read_key():
            case "up":
                selector[current] = " "
                selector[current-1] = ">"
                print_start()
                sleep()
            case "down":
                selector[current] = " "
                if current != 3:
                    selector[current+1] = ">"
                else:
                    selector[0] = ">"
                print_start()
                sleep()
            case "space":
                match current:
                    case 0:
                        os.system("cls")
                        print("3")
                        time.sleep(1)
                        os.system("cls")
                        print("2")
                        time.sleep(1)
                        os.system("cls")
                        print("1")
                        time.sleep(1)
                        os.system("cls")
                        game()
                        result(game=True)
                        print_start()
                    case 1:
                        result()
                        print_start()
                    case 2:
                        operation()
                        print_start()
                    case 3:
                        return

def file(mode: str, data: list[dict[str:str]]=None) -> list[dict[str:str]] | None:
    if mode == "read":
        with open("data.json", encoding="UTF-8") as f:
            save: list[dict[str:str]] = json.load(f)
        return save
    else:
        with open("data.json", "w", encoding="UTF-8") as f:
            json.dump(data, f) if data != None else None
        return

if __name__ == "__main__":
    main()
