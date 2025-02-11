import copy
import json
import keyboard # required
import os
import random
import threading
import time
import traceback
import winsound

class Minos:
    def __init__(self, shape: str) -> None:
        self.depth: int = 0
        self.down: bool = False
        self.left: bool = False
        self.right: bool = False
        self.rotate: bool = False
        self.rotated: int = 0
        self.shape: str = shape
        self.x: int = 4 if shape in {"O", "Z"} else 3
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

    def hold(self, shape: str) -> bool:
        can: bool = False
        self.deploy(remove=True)
        match shape:
            case "I":
                if self.x+3 <= 9:
                    for i in range(3):
                        if stage[self.depth][self.x+i] == "=":
                            break
                    else:
                        can = True
            case "O":
                if self.x+1 <= 9:
                    for i in range(2):
                        for j in range(2):
                            if stage[self.depth+i][self.x+j] == "=":
                                break
                    else:
                        can = True
            case "T":
                if (self.x+2 <= 9) & (stage[self.depth][self.x+1] != "="):
                    for i in range(3):
                        if stage[self.depth+1][self.x+i] == "=":
                            break
                    else:
                        can = True
            case "S":
                if self.x+2 <= 9:
                    for i in range(2):
                        for j in range(2):
                            if stage[self.depth+i][self.x-i+j+1] == "=":
                                break
                    else:
                        can = True
            case "Z":
                if self.x+2 <= 9:
                    for i in range(2):
                        for j in range(2):
                            if stage[self.depth+i][self.x+i+j] == "=":
                                break
                    else:
                        can = True
            case "J":
                if (self.x+2 <= 9) & (stage[self.depth][self.x] != "="):
                    for i in range(3):
                        if stage[self.depth+1][self.x+i] == "=":
                            break
                    else:
                        can = True
            case "L":
                if (self.x+2 <= 9) & (stage[self.depth][self.x+2] != "="):
                    for i in range(3):
                        if stage[self.depth+1][self.x+i] == "=":
                            break
                    else:
                        can = True
        if can:
            self.shape = shape
            self.rotated = 0
            self.deploy()
            return True
        else:
            return False

    def move(self, direction: str) -> None:
        match direction:
            case "left":
                self.deploy(remove=True)
                self.x -= 1
                self.deploy()
            case "right":
                self.deploy(remove=True)
                self.x += 1
                self.deploy()
            case "rotate":
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

def game() -> None:
    def key_input() -> None:
        nonlocal alive, can, hold, index, pause, paused
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
                    flag()
                    if can:
                        old = hold
                        if hold == "N":
                            hold = mino.shape
                            if mino.hold(shape=shapes[index]) if (not mino.left) & (not mino.right) & (not mino.down) else False:
                                index += 1 if index != 6 else -6
                                can = False
                            else:
                                hold = old
                        else:
                            hold = mino.shape
                            if mino.hold(shape=old) if (not mino.left) & (not mino.right) & (not mino.down) else False:
                                can = False
                            else:
                                hold = old
                    print_stage()
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
                                sleep()
                                break
        return

    def line() -> None:
        nonlocal level, point
        row: int = 0
        for i in range(20):
            if " " not in stage[i]:
                row += 1
                stage.pop(i)
                stage.insert(0, [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "])
                point += level * 100 * row if level != 0 else 100 * row
                if level <= 15:
                    level = point // 10000
                else:
                    level = 15
        if stage[19] == [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]:
            point += level * 1000 if level != 0 else 1000
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
                    match shapes[index]:
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
                    match shapes[index]:
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
                    match shapes[index]:
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
        return

    global stage
    alive: bool = True
    can: bool = True
    flag = lambda: mino.flag()
    hold: str = "N"
    index: int = 0
    key = threading.Thread(target=key_input, daemon=True)
    level: int = 0
    pause: bool = False
    paused: bool= False
    point: float = 0.0
    shapes: list[str] = ["I", "O", "T", "S", "Z", "J", "L"]
    shuffle = lambda: random.shuffle(shapes)
    stage = copy.deepcopy(STAGE)
    key.start()
    shuffle()
    winsound.PlaySound("bgm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    while True:
        print_stage()
        mino: Minos = Minos(shapes[index])
        index += 1
        if index == 7:
            shuffle()
            index = 0
        line()
        flag()
        if mino.down:
            alive = False
            print_stage()
            save() if not paused else None
            break
        while (not mino.down) & alive:
            print_stage()
            time.sleep(2 - level * 0.1)
            mino.move("down") if (not mino.down) & (not pause) else None
            flag()
        can = True
        line()
        print_stage()
        sleep()
    key.join()
    winsound.PlaySound(None, winsound.SND_PURGE)
    return

def result(game: bool=False) -> None:
    data: list[dict[str:str]] = file("read")
    os.system("cls")
    if data == []:
        print("- - -  N O  D A T A  - - -")
    else:
        print("- - - G A M E  O V E R  - - -") if game else None
        print("- - -  R E S U L T  - - -\n")
        for d in data:
            print(f"{d["date"]}: {d["point"]}")
    print("\n[P R E S S  E S C  K E Y  T O  R E T U R N]")

    print("[P R E S S  B A C K S P A C E  K E Y  T O  D E L E T E  S A V E  D A T A]")
    while True:
        if keyboard.read_key() == "esc":
            break
        elif keyboard.read_key() == "backspace":
            file("write", [])
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
        with open("save.dat", encoding="UTF-8") as f:
            save: list[dict[str:str]] = json.load(f)
        return save
    else:
        with open("save.dat", "w", encoding="UTF-8") as f:
            json.dump(data, f) if data != None else None
        return

STAGE: list[list[str]] = [
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
selector: list[str] = [">", " ", " ", " "]
sleep = lambda: time.sleep(0.12)
if __name__ == "__main__":
    try: main()
    except Exception:
        with open("error.log", "w", encoding="UTF-8") as f:
            f.write(f"{time.strftime("%Y-%m-%d %H:%M:%S")}\n{traceback.format_exc()}")
